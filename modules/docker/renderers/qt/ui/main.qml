import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.12

ApplicationWindow {
    width: 800
    height: 600
    id: mainWindow
    title: "Edit dockers"
    visible: true
    SplitView {
        id: mainSplit
        anchors.fill: parent
        orientation: Qt.Horizontal

        ListView {
            id: listView
            width: parent.width/2
            height: parent.height
            clip: false
            spacing: 8
            model: ListModel {
                ListElement {
                    name: "Grey"
                    colorCode: "grey"
                }

                ListElement {
                    name: "Red"
                    colorCode: "red"
                }

                ListElement {
                    name: "Blue"
                    colorCode: "blue"
                }

                ListElement {
                    name: "Green"
                    colorCode: "green"
                }
            }
            delegate: Item {
                x: 5
                width: 80
                height: 40
                Row {
                    id: row1
                    Rectangle {
                        width: 40
                        height: 40
                        color: colorCode
                    }

                    Text {
                        text: name
                        anchors.verticalCenter: parent.verticalCenter
                        font.bold: true
                    }
                    spacing: 10
                }
            }
        }

        Item {
            id: item2
            width: parent.width/2
            height: parent.height/2
            Rectangle
            {
                anchors.fill: parent
                color: "blue"
            }
        }
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:12}
}
##^##*/
