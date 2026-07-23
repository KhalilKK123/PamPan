package com.pampan.pampan.domain

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test
import java.math.BigDecimal
import java.time.LocalDate

class PantryContractTest {
    @Test
    fun quantityAndDateParsingPreserveExactApprovedValues() {
        assertEquals("0", PantryContract.parseQuantity("0").toPlainString())
        assertEquals("1.500", PantryContract.parseQuantity("1.500").toPlainString())
        assertEquals("1", PantryContract.parseQuantity("01").toPlainString())
        assertEquals("0.5", PantryContract.parseQuantity(".5").toPlainString())
        assertEquals("1", PantryContract.parseQuantity("1.").toPlainString())
        assertEquals("1000", PantryContract.parseQuantity("1e3").toPlainString())
        assertEquals("1.25", PantryContract.parseQuantity("+1.25").toPlainString())
        assertEquals(LocalDate.of(2026, 8, 15), PantryContract.parseExpiryDate("2026-08-15"))
    }

    @Test
    fun invalidQuantityAndDateFormsAreRejected() {
        listOf("-1", "", " ", "1.2.3", "NaN", " one ").forEach { value ->
            assertThrows(IllegalArgumentException::class.java) {
                PantryContract.parseQuantity(value)
            }
        }
        listOf("2026-8-15", "2026-02-30", "0000-01-01", "+10000-01-01", "not-a-date").forEach { value ->
            assertThrows(IllegalArgumentException::class.java) {
                PantryContract.parseExpiryDate(value)
            }
        }
    }

    @Test
    fun blankFieldsNegativeQuantitiesAndUntrimmedUnitsAreRejected() {
        assertThrows(IllegalArgumentException::class.java) {
            PantryCategory(id = " ", name = "Produce")
        }
        assertThrows(IllegalArgumentException::class.java) {
            PantryCategory(id = "category-produce", name = "")
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(id = " ", quantity = BigDecimal.ONE)
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(name = "\t", quantity = BigDecimal.ONE)
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(quantity = BigDecimal("-0.1"))
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(quantity = BigDecimal.ONE, unit = " kg")
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(quantity = BigDecimal.ONE, categoryId = "")
        }
    }

    @Test
    fun snapshotRequiresUniqueIdsAndResolvedCategories() {
        val category = PantryCategory(id = "category-produce", name = "Produce")
        assertThrows(IllegalArgumentException::class.java) {
            PantrySnapshot(categories = listOf(category, category), items = emptyList())
        }
        val pantryItem = item(quantity = BigDecimal.ZERO)
        assertThrows(IllegalArgumentException::class.java) {
            PantrySnapshot(categories = listOf(category), items = listOf(pantryItem, pantryItem))
        }
        assertThrows(IllegalArgumentException::class.java) {
            PantrySnapshot(
                categories = listOf(category),
                items = listOf(item(quantity = BigDecimal.ZERO, categoryId = "category-missing")),
            )
        }
    }

    @Test
    fun resolvedItemsPreserveOrderCaseAndDecimalScale() {
        val categories =
            listOf(
                PantryCategory(id = "category-one", name = "First"),
                PantryCategory(id = "category-two", name = "Second"),
            )
        val items =
            listOf(
                item(
                    id = "item-one",
                    name = "One",
                    quantity = BigDecimal("1.50"),
                    unit = "mL",
                    categoryId = "category-two",
                ),
                item(
                    id = "item-two",
                    name = "Two",
                    quantity = BigDecimal.ZERO,
                    unit = "pieces",
                    categoryId = "category-one",
                ),
            )

        val resolved = PantrySnapshot(categories, items).resolvedItems()

        assertEquals(listOf("item-one", "item-two"), resolved.map(PantryPreviewItem::id))
        assertEquals("1.50", resolved.first().quantity)
        assertEquals("mL", resolved.first().unit)
        assertEquals("Second", resolved.first().categoryName)
    }

    private fun item(
        id: String = "item",
        name: String = "Item",
        quantity: BigDecimal,
        unit: String = "kg",
        categoryId: String = "category-produce",
    ) = PantryItem(
        id = id,
        name = name,
        quantity = quantity,
        unit = unit,
        expiryDate = LocalDate.of(2026, 8, 15),
        categoryId = categoryId,
    )
}
