import SwiftUI

@main
struct ClosetPreviewApp: App {
    var body: some Scene {
        WindowGroup {
            // Replace with real token from login result.
            let api = APIClient(baseURL: URL(string: "http://127.0.0.1:8000")!, accessToken: "replace-with-access-token")
            ClosetPreviewView(viewModel: ClosetPreviewViewModel(api: api, userId: "replace-with-user-id"))
        }
    }
}
