import SwiftUI

struct ClosetPreviewView: View {
    @StateObject var viewModel: ClosetPreviewViewModel

    var body: some View {
        GeometryReader { proxy in
            HStack(spacing: 12) {
                leftPanel(width: proxy.size.width * 0.42)
                rightPanel(width: proxy.size.width * 0.58)
            }
            .padding(12)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(DesignTokens.pageBackground)
            .task { await viewModel.loadItems() }
        }
    }

    private func leftPanel(width: CGFloat) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("衣橱")
                .font(.title3.bold())
                .foregroundStyle(DesignTokens.primaryText)

            ScrollView {
                LazyVStack(spacing: 10) {
                    ForEach(viewModel.items) { item in
                        Button {
                            viewModel.select(item)
                        } label: {
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(item.name)
                                        .font(.subheadline.weight(.semibold))
                                        .foregroundStyle(DesignTokens.primaryText)
                                    Text(item.rarity)
                                        .font(.caption)
                                        .foregroundStyle(DesignTokens.secondaryText)
                                }
                                Spacer()
                                if item.isWearing {
                                    Text("已穿戴")
                                        .font(.caption2)
                                        .padding(.horizontal, 8)
                                        .padding(.vertical, 4)
                                        .background(DesignTokens.accent.opacity(0.25))
                                        .clipShape(Capsule())
                                        .foregroundStyle(DesignTokens.primaryText)
                                }
                            }
                            .padding(12)
                            .frame(maxWidth: .infinity)
                            .background(DesignTokens.cardBackground)
                            .overlay(RoundedRectangle(cornerRadius: 12).stroke(DesignTokens.cardBorder, lineWidth: 1))
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                        }
                    }
                }
            }
        }
        .padding(12)
        .frame(width: width)
        .background(DesignTokens.panelBackground.opacity(0.45))
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }

    private func rightPanel(width: CGFloat) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("右侧即时预览")
                .font(.title3.bold())
                .foregroundStyle(DesignTokens.primaryText)

            Group {
                switch viewModel.previewState {
                case .idle:
                    stateCard(text: "请选择左侧服装，右侧将实时生成最终样式")
                case .loading:
                    ProgressView("生成中...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                case .failure(let message):
                    stateCard(text: "预览失败：\(message)")
                case .success(let preview):
                    VStack(alignment: .leading, spacing: 10) {
                        AsyncImage(url: URL(string: preview.previewImageUrl)) { image in
                            image.resizable().scaledToFit()
                        } placeholder: {
                            Rectangle().fill(Color.white.opacity(0.08))
                                .overlay(ProgressView())
                        }
                        .frame(maxWidth: .infinity, minHeight: 300)
                        .clipShape(RoundedRectangle(cornerRadius: 14))

                        Text("单品：\(preview.itemName)")
                            .foregroundStyle(DesignTokens.primaryText)
                        Text("渲染引擎：\(preview.renderEngine)")
                            .font(.caption)
                            .foregroundStyle(DesignTokens.secondaryText)
                    }
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .padding(12)
        .frame(width: width)
        .background(DesignTokens.panelBackground.opacity(0.4))
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }

    private func stateCard(text: String) -> some View {
        Text(text)
            .foregroundStyle(DesignTokens.secondaryText)
            .font(.subheadline)
            .multilineTextAlignment(.center)
            .padding(20)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(DesignTokens.cardBackground)
            .clipShape(RoundedRectangle(cornerRadius: 14))
    }
}

#Preview {
    let api = APIClient(baseURL: URL(string: "http://127.0.0.1:8000")!, accessToken: "demo-token")
    return ClosetPreviewView(viewModel: ClosetPreviewViewModel(api: api, userId: "usr_demo"))
}
