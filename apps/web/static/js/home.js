let currentSessionId = null;

function generateRandomString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
};

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
};

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
};

function getOrCreateSessionId() {
    let sessionId = getCookie('sessionId');

    if (sessionId) {
        return sessionId;
    } else {
        sessionId = generateRandomString(10);
        setCookie('sessionId', sessionId, 3650);
        return sessionId;
    }
};

function showToast(icon, title, text, action = null) {
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didClose: () => {
            if (action === 'reload') {
                window.location.reload();
            }
        }
    });

    Toast.fire({
        icon: icon,
        html: `
            <div class="d-flex flex-column gap-1">
                <p class="mb-0 fw-semibold">${title}</p>
                <p class="mb-0">${text}</p>
            </div>
        `
    });
};

document.addEventListener('DOMContentLoaded', () => {
    currentSessionId = getOrCreateSessionId();
    console.log(currentSessionId);
});

document.addEventListener('alpine:init', () => {
    Alpine.data('dreamInterpreter', () => ({
        loading: false,
        dreamDescription: '',
        interpretationResult: '',
        oldInterpretations: [],

        async getInterpretations() {
            this.loading = true;

            try {
                const response = await fetch('/api/interpretations/' + currentSessionId);
                const data = await response.json();

                if (!response.ok) {
                    showToast(data.type, data.title, data.message);
                    return;
                }

                this.oldInterpretations = data.interpretations;
                showToast(data.type, data.title, data.message);
            } catch {
                if (error instanceof TypeError && (error.message === 'Failed to fetch' || error.message.includes('network error'))) {
                    showToast('error', 'Error de red', 'Error al contactar con el servidor.')
                }
            } finally {
                this.loading = false;
            }
        },

        async interpretDream() {
            this.loading = true;
            
            const csrftoken = getCookie('csrftoken');

            try {
                const response = await fetch('/api/create/' ,{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        user: currentSessionId,
                        dream: this.dreamDescription
                    })
                });
                const data = await response.json();
                
                console.log(data);

                if (!response.ok) {
                    showToast(data.type, data.title, data.message, data.action ? data.action : null);
                    return;
                }

                this.interpretationResult = data.interpretation;
                showToast(data.type, data.title, data.message);
            } catch (error) {
                if (error instanceof TypeError && (error.message === 'Failed to fetch' || error.message.includes('network error'))) {
                    showToast('error', 'Error de red', 'Error al contactar con el servidor.')
                }
            } finally {
                this.loading = false;
            }
        },

        resetInterpreter() {
            this.oldInterpretations = [];
            this.interpretationResult = '';
            this.dreamDescription = '';
            this.loading = false;
        }
    }));
});