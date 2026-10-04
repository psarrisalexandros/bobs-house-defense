import UIKit
import Capacitor

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = BobViewController()
        window?.makeKeyAndVisible()

        SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)
    }

    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        SceneDelegateProxy.shared.scene(scene, openURLContexts: URLContexts)
    }

    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        SceneDelegateProxy.shared.scene(scene, continue: userActivity)
    }
}

/// The game's screen: full screen, landscape, with the save-copy plugin attached.
class BobViewController: CAPBridgeViewController {
    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(BobCloudPlugin())
    }
    override var prefersStatusBarHidden: Bool { true }
    override var prefersHomeIndicatorAutoHidden: Bool { true }
    /// one deliberate swipe is needed to leave the game, so a stray thumb on the edge does not
    override var preferredScreenEdgesDeferringSystemGestures: UIRectEdge { .all }
    override var supportedInterfaceOrientations: UIInterfaceOrientationMask { .landscape }
}

/// A copy of the save in the player's iCloud key-value store. It survives deleting and reinstalling the game,
/// and follows the player to a new iPhone. Nothing is stored when the player is not signed in to iCloud; the calls still succeed.
@objc(BobCloudPlugin)
public class BobCloudPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "BobCloudPlugin"
    public let jsName = "BobCloud"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "put", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "get", returnType: CAPPluginReturnPromise)
    ]
    private let kv = NSUbiquitousKeyValueStore.default

    override public func load() {
        kv.synchronize()
    }

    @objc func put(_ call: CAPPluginCall) {
        guard let key = call.getString("key"), let value = call.getString("value") else {
            call.reject("key and value are required")
            return
        }
        kv.set(value, forKey: key)
        call.resolve()
    }

    @objc func get(_ call: CAPPluginCall) {
        guard let key = call.getString("key") else {
            call.reject("key is required")
            return
        }
        kv.synchronize()
        if let value = kv.string(forKey: key) {
            call.resolve(["value": value])
        } else {
            call.resolve()
        }
    }
}
