package com.pampan.pampan

import com.pampan.pampan.ui.FoundationCopy
import org.junit.Assert.assertEquals
import org.junit.Test

class FoundationCopyTest {
    @Test
    fun foundationCopyIsDeterministic() {
        assertEquals("PamPan", FoundationCopy.TITLE)
        assertEquals("Native foundation", FoundationCopy.STATUS)
        assertEquals("Your pantry, thoughtfully managed.", FoundationCopy.MESSAGE)
    }
}
