import XCTest
@testable import PamPan

final class PamPanTests: XCTestCase {
    func testFoundationCopyIsDeterministic() {
        XCTAssertEqual(FoundationView.title, "PamPan")
        XCTAssertEqual(FoundationView.status, "Native foundation")
        XCTAssertEqual(FoundationView.message, "Your pantry, thoughtfully managed.")
    }
}
