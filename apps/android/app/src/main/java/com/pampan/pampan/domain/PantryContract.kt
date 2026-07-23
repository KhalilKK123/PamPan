package com.pampan.pampan.domain

import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException

object PantryContract {
    const val VERSION = "1"

    private val expiryDatePattern =
        Regex("^(?!0000)[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$")

    fun parseQuantity(value: String): PantryDecimal = PantryDecimal.parse(value)

    fun parseExpiryDate(value: String): LocalDate {
        require(expiryDatePattern.matches(value)) {
            "Expiry date must use exact four-digit ISO YYYY-MM-DD form."
        }
        val parsed =
            try {
                LocalDate.parse(value, DateTimeFormatter.ISO_LOCAL_DATE)
            } catch (error: DateTimeParseException) {
                throw IllegalArgumentException("Expiry date must be a real ISO YYYY-MM-DD date.", error)
            }
        require(parsed.toString() == value) {
            "Expiry date must use canonical ISO YYYY-MM-DD form."
        }
        return parsed
    }
}

@JvmInline
value class PantryDecimal private constructor(
    val value: String,
) {
    companion object {
        private val pattern =
            Regex("^\\+?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?$")

        fun parse(value: String): PantryDecimal {
            require(pattern.matches(value)) {
                "Quantity must be a nonnegative decimal string."
            }
            return PantryDecimal(value)
        }
    }
}

data class PantryCategory(
    val id: String,
    val name: String,
) {
    init {
        require(id.isNotBlank()) { "Category ID must be nonblank." }
        require(name.isNotBlank()) { "Category name must be nonblank." }
    }
}

data class PantryItem(
    val id: String,
    val name: String,
    val quantity: PantryDecimal,
    val unit: String,
    val expiryDate: LocalDate,
    val categoryId: String,
) {
    init {
        require(id.isNotBlank()) { "Item ID must be nonblank." }
        require(name.isNotBlank()) { "Item name must be nonblank." }
        require(unit.isNotBlank() && unit == unit.trim()) {
            "Unit must be trimmed and nonblank."
        }
        require(categoryId.isNotBlank()) { "Category ID must be nonblank." }
    }
}

data class PantrySnapshot(
    val categories: List<PantryCategory>,
    val items: List<PantryItem>,
) {
    init {
        require(categories.isNotEmpty()) { "At least one category is required." }
        require(categories.map(PantryCategory::id).toSet().size == categories.size) {
            "Category IDs must be unique."
        }
        require(items.map(PantryItem::id).toSet().size == items.size) {
            "Item IDs must be unique."
        }
        val categoryIds = categories.map(PantryCategory::id).toSet()
        require(items.all { it.categoryId in categoryIds }) {
            "Every item category ID must resolve to a category."
        }
    }

    fun resolvedItems(): List<PantryPreviewItem> {
        val categoriesById = categories.associateBy(PantryCategory::id)
        return items.map { item ->
            PantryPreviewItem(
                id = item.id,
                name = item.name,
                quantity = item.quantity.value,
                unit = item.unit,
                expiryDate = item.expiryDate.toString(),
                categoryName = checkNotNull(categoriesById[item.categoryId]).name,
            )
        }
    }
}

data class PantryPreviewItem(
    val id: String,
    val name: String,
    val quantity: String,
    val unit: String,
    val expiryDate: String,
    val categoryName: String,
)
