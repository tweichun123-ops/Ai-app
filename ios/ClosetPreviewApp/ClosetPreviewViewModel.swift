import SwiftUI

@MainActor
final class ClosetPreviewViewModel: ObservableObject {
    @Published var items: [ClosetItem] = []
    @Published var selectedItem: ClosetItem?
    @Published var previewState: PreviewState = .idle

    private let api: APIClient
    private let userId: String

    init(api: APIClient, userId: String) {
        self.api = api
        self.userId = userId
    }

    func loadItems() async {
        do {
            items = try await api.fetchClosetItems(userId: userId)
        } catch {
            previewState = .failure(error.localizedDescription)
        }
    }

    func select(_ item: ClosetItem) {
        selectedItem = item
        Task {
            await generatePreview(for: item)
        }
    }

    private func generatePreview(for item: ClosetItem) async {
        previewState = .loading
        do {
            let preview = try await api.tryOn(userId: userId, itemCode: item.itemCode)
            previewState = .success(preview)
        } catch {
            previewState = .failure(error.localizedDescription)
        }
    }
}
