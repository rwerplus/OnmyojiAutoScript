import QtQuick
import QtQuick.Controls
import FluentUI
import "../Component"

Item {

    MirrorImage{
        id: mirrorImage
        anchors{
            left: parent.left
            top: parent.top
        }
        width: 1280
        height: 720 + 50
        imageWidth: 1280
        imageHeight: 720

        onRoi_red_changed: function(roi){
            if(typeof ruleFile.currentItem === "undefined"){
                return
            }
            ruleFile.currentItem.roiFront = roi
        }

        onRoi_green_changed: function(roi){
            if(typeof ruleFile.currentItem === "undefined"){
                return
            }
            ruleFile.currentItem.roiBack = roi
        }
    }
    RuleFile{
        id: ruleFile
        anchors{
            left: mirrorImage.right
            leftMargin: 10
            right: parent.right
            top: parent.top
        }
        height: 600
        addFunc: add
        editFunc: edit
        saveFunc: save

        onCurrentItemChanged: {
            if(currentItem === "" || typeof currentItem === "undefined"){
                return
            }
            var [x, y, width, height] = currentItem.roiFront.split(',')
            mirrorImage.roiRed_x = parseInt(x)
            mirrorImage.roiRed_y = parseInt(y)
            mirrorImage.roiRed_width = parseInt(width)
            mirrorImage.roiRed_height = parseInt(height)
            var [x, y, width, height] = currentItem.roiBack.split(',')
            mirrorImage.roiGreen_x = parseInt(x)
            mirrorImage.roiGreen_y = parseInt(y)
            mirrorImage.roiGreen_width = parseInt(width)
            mirrorImage.roiGreen_height = parseInt(height)

        }
    }

    FluArea {
        id: ruleArea
        anchors{
            left: mirrorImage.right
            leftMargin: 10
            right: parent.right
            top: ruleFile.bottom
            topMargin: 12
            bottom: parent.bottom
        }
        Column{
            id: coi
            anchors{
                top: parent.top
                bottom: parent.bottom
                left: parent.left
                leftMargin: 20
                right: parent.right
                rightMargin: 20
            }
            spacing: 5
            //头
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Editing rule"
                    font: FluTextStyle.Subtitle
                }
            }
            //item name 这个参数项的名称
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Item name"
                    font: FluTextStyle.BodyStrong
                }
                FluTextBox{
                    id: itemName
                    anchors{
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                    placeholderText:"单行输入框"
                    disabled: true
                    text: (typeof ruleFile.currentItem === "undefined")? "" : ruleFile.currentItem.itemName
                    width: 200
                }
            }

            // roi front
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Roi front"
                    font: FluTextStyle.BodyStrong
                }
                FluTextBox{
                    id: roiFront
                    anchors{
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                    disabled: true
                    text:(typeof ruleFile.currentItem === "undefined")? "" : ruleFile.currentItem.roiFront
                    placeholderText:"0,0,100,100"
                    width: 200
                }
            }
            //roi back
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Roi Back"
                    font: FluTextStyle.BodyStrong
                }
                FluTextBox{
                    id: roiBack
                    anchors{
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                    disabled: true
                    text:(typeof ruleFile.currentItem === "undefined")? "" : ruleFile.currentItem.roiBack
                    placeholderText:"0,0,100,100"
                    width: 200


                }
            }
            //ocr 模式
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Mode"
                    font: FluTextStyle.BodyStrong
                }
                FComboBox{
                    id: mode
                    anchors{
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                    width: 200
                    model: ["Single", "Full", "Digit", "DigitCounter", "Duration"]
                    currentIndex: if(typeof ruleFile.currentItem !== "undefined"){
                                     if(ruleFile.currentItem.mode === "Single"){
                                         return 0
                                     }else if(ruleFile.currentItem.mode === "Full"){
                                         return 1
                                     }else if(ruleFile.currentItem.mode === "Digit"){
                                         return 2
                                     }else if(ruleFile.currentItem.mode === "DigitCounter"){
                                         return 3
                                     }else if(ruleFile.currentItem.mode === "Duration"){
                                         return 4
                                     }
                                  }else{return 0}
                    onActivated: {
                        if(currentIndex === 0){
                            ruleFile.currentItem.mode = "Single"
                        }
                        else if(currentIndex === 1){
                            ruleFile.currentItem.mode = "Full"
                        }
                        else if(currentIndex === 1){
                            ruleFile.currentItem.mode = "Digit"
                        }
                        else if(currentIndex === 1){
                            ruleFile.currentItem.mode = "DigitCounter"
                        }
                        else if(currentIndex === 1){
                            ruleFile.currentItem.mode = "Duration"
                        }
                    }
                }
            }
            // ocr 方法
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Method"
                    font: FluTextStyle.BodyStrong
                }
                FComboBox{
                    id: method
                    anchors{
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                    width: 200
                    currentIndex: 0
                    model: ["Default"]
                    onActivated: {

                    }
                }
            }
            //keyword 匹配字段
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Keyword"
                    font: FluTextStyle.BodyStrong
                }
                FluTextBox{
                    id: keyword
                    anchors{
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                    width: 200
                    text:(typeof ruleFile.currentItem === "undefined")? "" : ruleFile.currentItem.keyword
                    placeholderText:""
                    onEditingFinished: {
                        if(typeof ruleFile.currentItem === "undefined"){
                            return
                        }
                        ruleFile.currentItem.keyword = text
                    }
                }
            }

            //描述 description
            Item{
                width: coi.width
                height: 40
                FluText{
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Description"
                    font: FluTextStyle.BodyStrong
                }
                FluTextBox{
                    id: description
                    anchors{
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                    width: 200
                    text:(typeof ruleFile.currentItem === "undefined")? "" : ruleFile.currentItem.description
                    placeholderText:"input your description"
                    onEditingFinished: {
                        if(typeof ruleFile.currentItem === "undefined"){
                            return
                        }
                        ruleFile.currentItem.description = text
                    }
                }
            }

        }

    }

    // 帮助
    FluArea{
        id: ruleHelp
        anchors{
            left: parent.left
            right: ruleArea.left
            rightMargin: 10
            top: mirrorImage.bottom
            topMargin: 10
            bottom: parent.bottom
        }
        FluText{
            leftPadding: 12
            topPadding: 12
            text: "红色的框(Roi front = roi)表示这一个项OCR识别的默认范围，绿色的框(Roi Back = area)表示如果识别到会点击的的范围。
在移动边框时右边的roi并不会实时显示，当切换软件的焦点时更新显示，但是具体的数值是更新的。
投屏的设置最上边点击即可"
        }

    }

    function add(){
        const item ={}
        item["itemName"] = "new-ocr-item"
        item["roiFront"] = "0,0,100,100"
        item["roiBack"] = "0,0,100,100"
        item["mode"] = "Single"
        item["method"] = "Default"
        item["keyword"] = ""
        item["description"] = "Ocr-description"
        showSuccess("Add new item")
        return item
    }

    function edit(model){

    }

    function save(){
        const data = []
        for(var i=0; i<ruleFile.list_model.count; i++){
            const item = ruleFile.list_model.get(i)
            const itemData = {}
            itemData["itemName"] = item["itemName"]
            itemData["roiFront"] = item["roiFront"]
            itemData["roiBack"] = item["roiBack"]
            itemData["mode"] = item["mode"]
            itemData["method"] = item["method"]
            itemData["keyword"] = item["keyword"]
            itemData["description"] = item["description"]
            data.push(itemData)
        }

        ruleFile.rule_file.write_file(ruleFile.file, JSON.stringify(data, null, "  "))
        showSuccess("Save file")

    }


}
