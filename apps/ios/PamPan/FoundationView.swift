import SwiftUI

struct FoundationView: View {
    static let title = "PamPan"
    static let status = "Native foundation"
    static let message = "Your pantry, thoughtfully managed."

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "cabinet.fill")
                .font(.system(size: 48, weight: .semibold))
                .foregroundStyle(.green)
                .accessibilityHidden(true)

            Text(Self.title)
                .font(.largeTitle.bold())

            Text(Self.status)
                .font(.headline)

            Text(Self.message)
                .font(.body)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding(24)
    }
}

#Preview {
    FoundationView()
}
