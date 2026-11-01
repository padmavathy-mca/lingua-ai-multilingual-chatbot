

(function () {
    "use strict";

    // 1. Multilingual keyboard layouts
    const layouts = {
        Tamil: [
            Array.from("அஆஇஈஉஊஎஏஐஒஓஔ"),
            Array.from("கஙசஞடணதநபம"),
            Array.from("யரலவழளறனஜஷஸஹ"),
            Array.from("ாிீுூெேைொோௌ்")
        ],

        Hindi: [
            Array.from("अआइईउऊऋएऐओऔ"),
            Array.from("कखगघङचछजझञ"),
            Array.from("टठडढणतथदधन"),
            Array.from("पफबभमयरलवशषसह"),
            Array.from("ािीुूृेैोौंः्")
        ],

        Telugu: [
            Array.from("అఆఇఈఉఊఋఎఏఐఒఓఔ"),
            Array.from("కఖగఘఙచఛజఝఞ"),
            Array.from("టఠడఢణతథదధన"),
            Array.from("పఫబభమయరలవశషసహ"),
            Array.from("ాిీుూృెేైొోౌంః్")
        ],

        Malayalam: [
            Array.from("അആഇഈഉഊഋഎഏഐഒഓഔ"),
            Array.from("കഖഗഘങചഛജഝഞ"),
            Array.from("ടഠഡഢണതഥദധന"),
            Array.from("പഫബഭമയരലവശഷസഹളഴറ"),
            Array.from("ാിീുൂൃെേൈൊോൌംഃ്")
        ]
    };

    // 2. Get HTML elements
    const languageSelect = document.getElementById("language");
    const keyboard = document.getElementById("keyboard");
    const message = document.getElementById("message");
    const keyboardPanel = document.getElementById("keyboardPanel");
    const toggleKeyboard = document.getElementById("toggleKeyboard");

    const spaceButton = document.getElementById("space");
    const backspaceButton = document.getElementById("backspace");
    const clearButton = document.getElementById("clear");
    const sendButton = document.getElementById("send");

    // 3. Validate required HTML elements
    const requiredElements = {
        languageSelect,
        keyboard,
        message,
        toggleKeyboard,
        spaceButton,
        backspaceButton,
        clearButton,
        sendButton
    };

    for (const [name, element] of Object.entries(requiredElements)) {
        if (!element) {
            console.error("Missing HTML element:", name);
            return;
        }
    }

    let currentLanguage = layouts[languageSelect.value]
        ? languageSelect.value
        : "Tamil";

    // 4. Keyboard toggle
    toggleKeyboard.addEventListener("click", () => {
        const isHidden =
            window.getComputedStyle(keyboardPanel).display === "none";

        keyboardPanel.style.display = isHidden ? "block" : "none";

        toggleKeyboard.setAttribute(
            "aria-expanded",
            String(isHidden)
        );
    });

    // 5. Render keyboard
    function renderKeyboard() {
        keyboard.innerHTML = "";

        const rows = layouts[currentLanguage];

        rows.forEach(row => {
            const rowElement = document.createElement("div");
            rowElement.className = "keyboard-row";

            row.forEach(character => {
                const button = document.createElement("button");

                button.type = "button";
                button.className = "key";
                button.textContent = character;

                button.addEventListener("click", () => {
                    insertText(character);
                });

                rowElement.appendChild(button);
            });

            keyboard.appendChild(rowElement);
        });
    }

    // 6. Insert characters at cursor position
    function insertText(text) {
        const start = message.selectionStart;
        const end = message.selectionEnd;

        message.setRangeText(text, start, end, "end");
        message.focus();
    }

    // 7. Language selection
    languageSelect.addEventListener("change", function () {
        if (layouts[this.value]) {
            currentLanguage = this.value;
            renderKeyboard();
        }
    });

    // 8. Space button
    spaceButton.addEventListener("click", () => {
        insertText(" ");
    });

    // 9. Backspace button
    backspaceButton.addEventListener("click", () => {
        const start = message.selectionStart;
        const end = message.selectionEnd;

        if (start !== end) {
            message.setRangeText("", start, end, "end");
        } else if (start > 0) {
            const chars = Array.from(message.value);
            const before = chars.slice(0, start);
            const after = chars.slice(start);

            before.pop();

            message.value = before.join("") + after.join("");

            const position = before.join("").length;
            message.setSelectionRange(position, position);
        }

        message.focus();
    });

    // 10. Clear button
    clearButton.addEventListener("click", () => {
        message.value = "";
        message.focus();
    });

    // 11. Send message to Streamlit
    sendButton.addEventListener("click", () => {
        const finalText = message.value.trim();

        if (!finalText) {
            return;
        }

        console.log("Sending message to Streamlit:", finalText);

        window.parent.postMessage({
            isStreamlitMessage: true,
            type: "streamlit:setComponentValue",
            value: {
                text: finalText,
                language: currentLanguage,
                submitted: true,
                submission_id: Date.now()
            }
        }, "*");
    });

    // 12. Listen for Streamlit render events
    window.addEventListener("message", function (event) {
        if (!event.data || event.data.type !== "streamlit:render") {
            return;
        }

        const args = event.data.args || {};

        if (args.language && layouts[args.language]) {
            currentLanguage = args.language;
            languageSelect.value = currentLanguage;
            renderKeyboard();
        }
    });

    // 13. Initial keyboard rendering
    renderKeyboard();

    // 14. Notify Streamlit that component is ready
    window.parent.postMessage({
        isStreamlitMessage: true,
        type: "streamlit:componentReady",
        apiVersion: 1
    }, "*");

    // 15. Set component height
    window.parent.postMessage({
        isStreamlitMessage: true,
        type: "streamlit:setFrameHeight",
        height: 550
    }, "*");

    console.log("Lingua AI component ready");

})();
