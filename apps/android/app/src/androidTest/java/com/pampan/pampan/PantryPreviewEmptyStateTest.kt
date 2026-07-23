package com.pampan.pampan

import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsNotDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performScrollTo
import androidx.compose.ui.unit.Density
import com.pampan.pampan.domain.PantryPreviewItem
import com.pampan.pampan.ui.PantryPreviewCopy
import com.pampan.pampan.ui.PantryPreviewScreen
import com.pampan.pampan.ui.PantryPreviewTestTags
import com.pampan.pampan.ui.theme.PamPanTheme
import org.junit.Rule
import org.junit.Test

class PantryPreviewEmptyStateTest {
    @get:Rule
    val composeRule = createComposeRule()

    @Test
    fun emptyPreviewDoesNotClaimLoadingNetworkOrPersistenceFailure() {
        showAtDoubleFontScale(items = emptyList())

        composeRule.onNodeWithText(PantryPreviewCopy.TITLE).assertIsDisplayed()
        composeRule.onNodeWithText(PantryPreviewCopy.STATUS).assertIsDisplayed()
        composeRule
            .onNodeWithTag(PantryPreviewTestTags.EMPTY)
            .assertIsDisplayed()
        composeRule.onNodeWithText("Loading", substring = true).assertIsNotDisplayed()
        composeRule.onNodeWithText("error", substring = true, ignoreCase = true).assertIsNotDisplayed()
    }

    @Test
    fun populatedContentRemainsReachableAtDoubleFontScale() {
        showAtDoubleFontScale(items = sampleItems)

        composeRule.onNodeWithText(PantryPreviewCopy.TITLE).assertIsDisplayed()
        composeRule.onNodeWithText(PantryPreviewCopy.STATUS).assertIsDisplayed()
        val itemNodes = composeRule.onAllNodesWithTag(PantryPreviewTestTags.ITEM)
        repeat(sampleItems.size) { index ->
            itemNodes[index].performScrollTo().assertIsDisplayed()
        }
    }

    private fun showAtDoubleFontScale(items: List<PantryPreviewItem>) {
        composeRule.setContent {
            val density = LocalDensity.current
            CompositionLocalProvider(
                LocalDensity provides Density(density = density.density, fontScale = 2f),
            ) {
                PamPanTheme {
                    PantryPreviewScreen(items = items)
                }
            }
        }
    }

    private val sampleItems =
        listOf(
            PantryPreviewItem(
                id = "item-green-apples",
                name = "Green apples",
                quantity = "6",
                unit = "pieces",
                expiryDate = "2026-08-15",
                categoryName = "Produce",
            ),
            PantryPreviewItem(
                id = "item-plain-yogurt",
                name = "Plain yogurt",
                quantity = "1.5",
                unit = "kg",
                expiryDate = "2026-08-04",
                categoryName = "Dairy",
            ),
            PantryPreviewItem(
                id = "item-brown-rice",
                name = "Brown rice",
                quantity = "2.25",
                unit = "kg",
                expiryDate = "2027-01-30",
                categoryName = "Pantry staples",
            ),
        )
}
