import Foundation

final class APIClient {
    let baseURL: URL
    let accessToken: String

    init(baseURL: URL, accessToken: String) {
        self.baseURL = baseURL
        self.accessToken = accessToken
    }

    func fetchClosetItems(userId: String, tab: String = "all") async throws -> [ClosetItem] {
        var components = URLComponents(url: baseURL.appendingPathComponent("api/users/\(userId)/closet/items"), resolvingAgainstBaseURL: false)
        components?.queryItems = [URLQueryItem(name: "tab", value: tab)]
        guard let url = components?.url else { throw URLError(.badURL) }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await URLSession.shared.data(for: request)
        try Self.ensureSuccess(response: response, data: data)
        return try JSONDecoder().decode(ClosetItemResponse.self, from: data).data.items
    }

    func tryOn(userId: String, itemCode: String) async throws -> TryOnPreview {
        let url = baseURL.appendingPathComponent("api/users/\(userId)/closet/try-on")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        request.httpBody = try JSONSerialization.data(withJSONObject: ["itemCode": itemCode])

        let (data, response) = try await URLSession.shared.data(for: request)
        try Self.ensureSuccess(response: response, data: data)
        return try JSONDecoder().decode(TryOnResponse.self, from: data).data
    }

    private static func ensureSuccess(response: URLResponse, data: Data) throws {
        guard let http = response as? HTTPURLResponse else { throw URLError(.badServerResponse) }
        guard (200...299).contains(http.statusCode) else {
            let message = String(data: data, encoding: .utf8) ?? "request failed"
            throw NSError(domain: "APIError", code: http.statusCode, userInfo: [NSLocalizedDescriptionKey: message])
        }
    }
}
