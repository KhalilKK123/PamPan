package com.pampan.pampan.domain

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test
import java.time.LocalDate

class PantryContractTest {
    @Test
    fun quantityAndDateParsingPreserveExactApprovedValues() {
        listOf("0", "1.500", "01", ".5", "1.", "1e3", "+1.25", "1e9999999999")
            .forEach { value ->
                assertEquals(value, PantryContract.parseQuantity(value).value)
            }
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
            item(id = " ")
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(name = "\t")
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(unit = " kg")
        }
        assertThrows(IllegalArgumentException::class.java) {
            item(categoryId = "")
        }
    }

    @Test
    fun snapshotRequiresUniqueIdsAndResolvedCategories() {
        val category = PantryCategory(id = "category-produce", name = "Produce")
        assertThrows(IllegalArgumentException::class.java) {
            PantrySnapshot(categories = listOf(category, category), items = emptyList())
        }
        val pantryItem = item()
        assertThrows(IllegalArgumentException::class.java) {
            PantrySnapshot(categories = listOf(category), items = listOf(pantryItem, pantryItem))
        }
        assertThrows(IllegalArgumentException::class.java) {
            PantrySnapshot(
                categories = listOf(category),
                items = listOf(item(categoryId = "category-missing")),
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
                    quantity = PantryContract.parseQuantity("1.50"),
                    unit = "mL",
                    categoryId = "category-two",
                ),
                item(
                    id = "item-two",
                    name = "Two",
                    quantity = PantryContract.parseQuantity("0"),
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
        quantity: PantryDecimal = PantryContract.parseQuantity("1"),
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
