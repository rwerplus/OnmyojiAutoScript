import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12
import FluentUI

// Lightweight twin of app.qml — same FluApp boot, but routes to ToolsWindow
// instead of MainWindow. Keep the routing object minimal: no nav, no script
// items, no Add dialog.
Window {
    id: app
    Component.onCompleted: {
        FluApp.init(app)
        FluTheme.frameless = ("windows" === Qt.platform.os)
        FluTheme.darkMode = FluDarkMode.System
        FluApp.routes = {
            "/": "./module/gui/qml/ToolsWindow.qml",
        }
        FluApp.initialRoute = "/"
        FluApp.run()
    }
}
