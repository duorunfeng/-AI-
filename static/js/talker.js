document.addEventListener('DOMContentLoaded', function() {
    // 将 selectEngine 函数绑定到 window 上以确保全局可用
    window.selectEngine = function(engineName) {
        console.log("Selected Engine: " + engineName);
        localStorage.setItem('selectedEngine', engineName);
        showNotification(`You have selected: ${engineName}`, 'info');

        fetch(`/api/select-engine`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ engine: engineName })
        })
        .then(response => {
            if (response.ok) {
                return response.json();  // 如果成功，返回JSON解析的响应数据
            } else {
                // 处理不同的错误状态码
                return response.json().then(data => {
                    throw new Error(data.detail || 'Something went wrong on API server!');
                });
            }
        })
        .then(data => {
            console.log(data);
            showNotification(data.message, 'success');  // 假设后端返回消息在data.message中
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification(error.message, 'error');  // 显示错误消息
        });
    };

    // 定义显示通知的函数
    function showNotification(message, type) {
        const notificationElement = document.getElementById('notification');
        notificationElement.innerText = message;
        notificationElement.className = `notification ${type}`;
        notificationElement.style.display = 'block';

        setTimeout(() => {
            notificationElement.style.display = 'none';
        }, 5000);
    }

    // 绑定按钮点击事件
    document.querySelectorAll('.modal-button').forEach(button => {
        button.addEventListener('click', function () {
            window.selectEngine(this.textContent.trim());
        });
    });
});
