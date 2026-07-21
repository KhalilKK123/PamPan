import XCTest

final class PamPanUITests: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    func testFoundationScreenLaunches() {
        let app = XCUIApplication()
        app.launch()

        XCTAssertTrue(app.staticTexts["PamPan"].waitForExistence(timeout: 5))
        XCTAssertTrue(app.staticTexts["Native foundation"].exists)
    }
}
