import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import FluentUI

// Top-level window for tools_gui.py. Hosts ONLY the rule editors that live
// behind the "Tools" menu in the full GUI — there is no Overview, no script
// instance picker, no Add/Settings dialog. Everything binds against the
// LiteContext registered as `process_manager`, which talks to a single
// in-process Device.
//
// The Content/*.qml files are reused as-is. They import "../Component" for
// MirrorImage / RuleFile, and reach into `process_manager.gui_mirror_image`
// for the live screenshot — which LiteContext provides.
FluWindow {
    id: window
    title: "OAS 工具"
    width: 1500
    height: 820
    minimumWidth: 1320
    minimumHeight: 760
    closeDestory: false
    launchMode: FluWindow.SingleTask

    FluAppBar {
        id: appbar
        z: 9
        width: parent.width
        title: "OAS 工具"
    }

    // --- Left: tool list -----------------------------------------------
    FluArea {
        id: menuArea
        width: 180
        anchors {
            left: parent.left
            top: appbar.bottom
            bottom: parent.bottom
            margins: 8
        }

        ListView {
            id: toolList
            anchors.fill: parent
            anchors.margins: 4
            spacing: 2
            clip: true
            model: [
                "图像规则",
                "文字识别",
                "点击规则",
                "长按规则",
                "滑动规则",
                "列表规则",
            ]

            property int activeIndex: 0
            currentIndex: activeIndex

            delegate: Rectangle {
                width: ListView.view.width
                height: 38
                radius: 4
                color: ListView.isCurrentItem ? FluTheme.primaryColor.lighter
                                              : (mouseArea.containsMouse ? Qt.rgba(0, 0, 0, 0.06)
                                                                          : "transparent")
                FluText {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 12
                    text: modelData
                    color: parent.ListView.isCurrentItem ? "white" : FluTheme.fontPrimaryColor
                }
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        toolList.activeIndex = index
                        loadTool(modelData)
                    }
                }
            }
        }
    }

    // --- Right: content loader ------------------------------------------
    Loader {
        id: contentLoader
        anchors {
            left: menuArea.right
            right: parent.right
            top: appbar.bottom
            bottom: parent.bottom
            leftMargin: 8
            rightMargin: 8
            topMargin: 8
            bottomMargin: 8
        }
        // Each Content/*.qml expects a parent with showSuccess()/showError() —
        // FluWindow provides those, and Loader inherits from window. Good.
    }

    // Map tool display name to its Content QML file. Chinese labels here
    // must match ToolsWindow's ListView model and lite_manager.TOOLS_MENU.
    function loadTool(name) {
        var fileMap = {
            "图像规则": "Content/ImageRule.qml",
            "文字识别": "Content/OcrRule.qml",
            "点击规则": "Content/ClickRule.qml",
            "长按规则": "Content/LongClickRule.qml",
            "滑动规则": "Content/SwipeRule.qml",
            "列表规则": "Content/ListRule.qml",
        }
        var file = fileMap[name]
        if (!file) {
            console.warn("Unknown tool:", name)
            return
        }
        // Re-load even when the file is the same so switching back resets
        // any half-edited state in the previous instance.
        contentLoader.source = ""
        contentLoader.source = file
    }

    Component.onCompleted: {
        // Honor --tool / profile.tool when set, otherwise fall back to 图像规则.
        var def = process_manager.default_tool ? process_manager.default_tool() : ""
        if (!def) def = "图像规则"
        // If the requested tool is unknown, loadTool() warns and we fall back.
        loadTool(def)
        if (process_manager.is_static_mode && process_manager.is_static_mode()) {
            window.title = "OAS 工具 (静态图: " + process_manager.static_image_path() + ")"
            appbar.title = window.title
        }
    }
}
