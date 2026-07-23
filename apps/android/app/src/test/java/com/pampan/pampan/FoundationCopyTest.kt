package com.pampan.pampan

import com.pampan.pampan.ui.PantryPreviewCopy
import org.junit.Assert.assertEquals
import org.junit.Test

class FoundationCopyTest {
    @Test
    fun previewCopyMakesTheSampleOnlyBoundaryExplicit() {
        assertEquals("Pantry preview", PantryPreviewCopy.TITLE)
        assertEquals("Sample data — not saved", PantryPreviewCopy.STATUS)
        assertEquals("No sample items to preview.", PantryPreviewCopy.EMPTY)
    }
}
