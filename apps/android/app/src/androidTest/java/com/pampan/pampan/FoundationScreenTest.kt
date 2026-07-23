package com.pampan.pampan

import androidx.compose.ui.test.assertContentDescriptionEquals
import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import com.pampan.pampan.ui.PantryPreviewCopy
import com.pampan.pampan.ui.PantryPreviewTestTags
import org.junit.Rule
import org.junit.Test

class FoundationScreenTest {
    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun offlinePreviewLaunchesWithCompleteSyntheticFixture() {
        composeRule.onNodeWithText(PantryPreviewCopy.TITLE).assertIsDisplayed()
        composeRule
            .onNodeWithTag(PantryPreviewTestTags.STATUS)
            .assertIsDisplayed()
        composeRule
            .onNodeWithText(PantryPreviewCopy.STATUS)
            .assertIsDisplayed()

        val items = composeRule.onAllNodesWithTag(PantryPreviewTestTags.ITEM)
        items.assertCountEquals(3)
        items[0].assertContentDescriptionEquals(
            "Green apples. Quantity 6 pieces. Expiry 2026-08-15. Category Produce.",
        )
        items[1].assertContentDescriptionEquals(
            "Plain yogurt. Quantity 1.5 kg. Expiry 2026-08-04. Category Dairy.",
        )
        items[2].assertContentDescriptionEquals(
            "Brown rice. Quantity 2.25 kg. Expiry 2027-01-30. Category Pantry staples.",
        )
    }
}
