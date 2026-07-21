package com.pampan.pampan

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.pampan.pampan.ui.FoundationScreen
import com.pampan.pampan.ui.theme.PamPanTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            PamPanTheme {
                FoundationScreen()
            }
        }
    }
}
