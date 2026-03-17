import Foundation

struct ClosetItem: Decodable, Identifiable, Hashable {
    let itemCode: String
    let name: String
    let rarity: String
    let tab: String
    let heartCost: Int
    let isFree: Bool
    let assetUrl: String
    let isWearing: Bool

    var id: String { itemCode }
}

struct ClosetItemResponse: Decodable {
    let data: ClosetData

    struct ClosetData: Decodable {
        let category: String
        let items: [ClosetItem]
        let tabs: [String]
    }
}

struct TryOnPreview: Decodable, Equatable {
    let itemCode: String
    let itemName: String
    let previewImageUrl: String
    let basePersonaImageUrl: String
    let clothAssetUrl: String
    let renderEngine: String
    let createdAt: String
}

struct TryOnResponse: Decodable {
    let data: TryOnPreview
}

enum PreviewState: Equatable {
    case idle
    case loading
    case success(TryOnPreview)
    case failure(String)
}
