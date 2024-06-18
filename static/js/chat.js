document.getElementById("stop-recording").disabled = true; // 初始设为禁用

const loadingIndicator = document.createElement("div");
loadingIndicator.id = "loading";
loadingIndicator.style.display = "none";
loadingIndicator.textContent = "加载中...";
document.body.appendChild(loadingIndicator);

let mediaRecorder;
let recordedChunks = [];

function showError(message) {
    console.error(message);
    displayMessage(message, "System");
}

async function submitText() {
    const textInput = document.getElementById("text-input");
    const text = textInput.value.trim();
    if (!text) return;

    displayMessage(text, "User");
    loadingIndicator.style.display = 'block';

    try {
        const response = await fetch("/api/process-user-text/", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        const data = await response.json();
        displayMessage(data.corrected_text, "System");
    } catch (error) {
        showError('Error processing text.');
    } finally {
        textInput.value = "";
        loadingIndicator.style.display = 'none';
    }
}

function displayMessage(message, sender) {
    if (!message) return;
    const messagesDiv = document.getElementById("messages");
    const messageParagraph = document.createElement("p");
    const currentTime = new Date().toLocaleTimeString();
    messageParagraph.textContent = `${sender}[${currentTime}]: ${message}`;
    messageParagraph.className = `message message-${sender.toLowerCase()}`;
    messagesDiv.appendChild(messageParagraph);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function updateLog(message) {   //关于输出视频制作时间
    const logDiv = document.getElementById("log-messages");
    const logEntry = document.createElement("p");
    logEntry.textContent = message;
    logDiv.appendChild(logEntry);
    logDiv.scrollTop = logDiv.scrollHeight;
}

document.getElementById("start-recording").addEventListener("click", async () => {
    console.log("Start recording button clicked.");
    document.getElementById("start-recording").disabled = true; // 禁用开始录音按钮
    document.getElementById("stop-recording").disabled = false; // 启用停止录音按钮
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        recordedChunks = [];
        console.log("MediaRecorder initialized.");

        mediaRecorder.ondataavailable = event => {
            recordedChunks.push(event.data);
            console.log("Data available from recording.");
        };
        mediaRecorder.onstop = async () => {
    console.log("Recording stopped, processing data.");
    const audioBlob = new Blob(recordedChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append("file", audioBlob, "audio.wav");

    try {
        const response = await fetch("/api/stop-recording/", {
            method: "POST",
            body: formData,
        });
        if (!response.ok) {
            console.error(`HTTP error! Status: ${response.status}`);
            displayMessage(`Failed to process the recording. Server error: ${response.status}`, "系统");
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (!data) {
            console.error("No data received from the server.");
            displayMessage("Failed to receive data from the server.", "System");
            return; // Early exit if no data received
        }

        console.log("Response received:", data);

        // Handle transcription text
        if (!data.transcribed_text) {
            console.warn("No transcription text received.");
            displayMessage("No transcription result available. Please check server logs.", "System");
        } else {
            console.log("Transcription successful:", data.transcribed_text);
            displayMessage(data.transcribed_text, "User");
            if (data.corrected_text) {
                displayMessage(data.corrected_text, "System");
            }
        }

        // Display processing times
        if (data.stt_processing_time) {
            updateLog(`STT processing time: ${data.stt_processing_time} seconds`);
        } else {
            console.warn("STT processing time not available.");
        }
        if (data.llm_processing_time) {
            updateLog(`LLM processing time: ${data.llm_processing_time} seconds`);
        } else {
            console.warn("LLM processing time not available.");
        }
        if (data.tts_processing_time) {
            updateLog(`TTS processing time: ${data.tts_processing_time} seconds`);
        } else {
            console.warn("TTS processing time not available.");
        }
        if (data.video_processing_time) {
            updateLog(`Video processing time: ${data.video_processing_time} seconds`);
        } else {
            console.warn("Video processing time not available.");
        }

        // Handle media paths
        if (data.audio_url) {
            const audioPlayer = document.getElementById('audio-player');
            const audioSource = audioPlayer.querySelector('source');
            audioSource.src = data.audio_url + `?${new Date().getTime()}`; // Append timestamp to avoid caching issues
            audioPlayer.load();
            audioPlayer.play();
        } else {
            console.warn("Audio path not available.");
        }

        if (data.video_url) {
            const videoPlayer = document.getElementById('video-player');
            const videoSource = videoPlayer.getElementsByTagName('source')[0];
            videoSource.src = data.video_url + `?${new Date().getTime()}`; // Append timestamp to avoid caching issues
            videoPlayer.load(); // Load the new video file
            videoPlayer.play(); // Optionally play the video
        } else {
            console.warn("Video URL not available.");
        }
    } catch (error) {
        console.error('Error uploading and transcribing:', error);
        displayMessage(`Error processing audio: ${error.message}`, "System");
    } finally {
        document.getElementById("start-recording").disabled = false;  // Re-enable the start recording button
        document.getElementById("stop-recording").disabled = true;   // Disable the stop recording button
        document.getElementById("text-input").value = "";  // Clear the text input field
    }
};



        mediaRecorder.start();
        console.log("Recording started.");
    } catch (error) {
        console.error("Unable to access the microphone(113):", error);
        showError("Unable to access the microphone.");
        document.getElementById("start-recording").disabled = false; // 重新启用开始录音按钮
        document.getElementById("stop-recording").disabled = true;   // 禁用停止录音按钮
    }
});

document.getElementById("stop-recording").addEventListener("click", () => {
    try {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            document.getElementById("start-recording").disabled = false;
            document.getElementById("stop-recording").disabled = true;
            console.log("Stopping recording...");
        }
    } catch (error) {
        console.error("Error during the recording or processing:", error);
    }
});

// 当文档加载完成后调用此函数
document.addEventListener('DOMContentLoaded', function() {
    updateCurrentEngineDisplay();
    setInterval(() => {
        updateCurrentEngineDisplay();
    }, 5000);  // 每5秒检查一次
});

function updateCurrentEngineDisplay() {
    // 尝试从 localStorage 获取存储的引擎名称
    const engineName = localStorage.getItem('selectedEngine') || 'None';
    // 获取显示引擎名称的 HTML 元素
    const engineDisplayElement = document.getElementById('currentEngineName');
    // 更新该元素的文本内容为当前选择的引擎名称
    engineDisplayElement.textContent = engineName;
}

