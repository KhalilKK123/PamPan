package com.pampan.pampan.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.pampan.pampan.domain.PantryPreviewItem

object PantryPreviewCopy {
    const val TITLE = "Pantry preview"
    const val STATUS = "Sample data — not saved"
    const val EMPTY = "No sample items to preview."
}

object PantryPreviewTestTags {
    const val STATUS = "pantry_preview_status"
    const val ITEM = "pantry_preview_item"
    const val EMPTY = "pantry_preview_empty"
}

@Suppress("ktlint:standard:function-naming")
@Composable
fun PantryPreviewScreen(
    items: List<PantryPreviewItem>,
    modifier: Modifier = Modifier,
) {
    Surface(modifier = modifier.fillMaxSize()) {
        Column(
            modifier =
                Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 24.dp, vertical = 32.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Text(
                text = PantryPreviewCopy.TITLE,
                modifier = Modifier.semantics { heading() },
                style = MaterialTheme.typography.headlineLarge,
                fontWeight = FontWeight.Bold,
            )
            Surface(
                modifier =
                    Modifier
                        .fillMaxWidth()
                        .testTag(PantryPreviewTestTags.STATUS),
                color = MaterialTheme.colorScheme.secondaryContainer,
                shape = MaterialTheme.shapes.medium,
            ) {
                Text(
                    text = PantryPreviewCopy.STATUS,
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    textAlign = TextAlign.Center,
                )
            }

            if (items.isEmpty()) {
                Text(
                    text = PantryPreviewCopy.EMPTY,
                    modifier =
                        Modifier
                            .fillMaxWidth()
                            .padding(vertical = 24.dp)
                            .testTag(PantryPreviewTestTags.EMPTY),
                    style = MaterialTheme.typography.bodyLarge,
                    textAlign = TextAlign.Center,
                )
            } else {
                items.forEach { item ->
                    PantryPreviewItemCard(item)
                }
            }
        }
    }
}

@Suppress("ktlint:standard:function-naming")
@Composable
private fun PantryPreviewItemCard(item: PantryPreviewItem) {
    val announcement =
        "${item.name}. Quantity ${item.quantity} ${item.unit}. " +
            "Expiry ${item.expiryDate}. Category ${item.categoryName}."
    Card(
        modifier =
            Modifier
                .fillMaxWidth()
                .testTag(PantryPreviewTestTags.ITEM)
                .semantics(mergeDescendants = true) {
                    contentDescription = announcement
                },
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text(
                text = item.name,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.SemiBold,
            )
            Text(
                text = "${item.quantity} ${item.unit}",
                style = MaterialTheme.typography.bodyLarge,
            )
            Text(
                text = "Expiry ${item.expiryDate}",
                style = MaterialTheme.typography.bodyMedium,
            )
            Text(
                text = "Category ${item.categoryName}",
                style = MaterialTheme.typography.bodyMedium,
            )
        }
    }
}
