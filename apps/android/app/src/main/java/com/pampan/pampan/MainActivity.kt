package com.pampan.pampan

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.pampan.pampan.data.PantryPreviewAsset
import com.pampan.pampan.ui.PantryPreviewScreen
import com.pampan.pampan.ui.theme.PamPanTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pantrySnapshot = PantryPreviewAsset.load(this)
        setContent {
            PamPanTheme {
                PantryPreviewScreen(items = pantrySnapshot.resolvedItems())
            }
        }
    }
}
