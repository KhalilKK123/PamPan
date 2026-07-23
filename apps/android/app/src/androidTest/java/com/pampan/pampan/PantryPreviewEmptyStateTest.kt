package com.pampan.pampan

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsNotDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
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
        composeRule.setContent {
            PamPanTheme {
                PantryPreviewScreen(items = emptyList())
            }
        }

        composeRule.onNodeWithText(PantryPreviewCopy.TITLE).assertIsDisplayed()
        composeRule.onNodeWithText(PantryPreviewCopy.STATUS).assertIsDisplayed()
        composeRule
            .onNodeWithTag(PantryPreviewTestTags.EMPTY)
            .assertIsDisplayed()
        composeRule.onNodeWithText("Loading", substring = true).assertIsNotDisplayed()
        composeRule.onNodeWithText("error", substring = true, ignoreCase = true).assertIsNotDisplayed()
    }
}
