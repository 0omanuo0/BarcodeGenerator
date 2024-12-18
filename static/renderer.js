document.getElementById('controls-form').addEventListener('submit', submitForm);


function submitForm(event) {
    if (event)
        event.preventDefault(); // Evita el envío predeterminado del formulario

    const formData = {
        barcode: document.getElementById('barcode').value,
        gap_x: document.getElementById('gap-x').value,
        gap_y: document.getElementById('gap-y').value,
        margin_x: document.getElementById('margin-x').value,
        margin_y: document.getElementById('margin-y').value,
        amount: document.getElementById('amount').value,
        rows: document.getElementById('rows').value,
        cols: document.getElementById('cols').value,
        draw_lines: document.getElementById('draw-lines').checked,
    };

    console.log('Form Data:', formData);

    // Enviar datos al servidor
    fetch('/generate-pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
        .then(response => {
            if (response.ok) {
                const pdf = document.getElementById('pdf-embed');

                // Refrescar el <embed> sin recargar la página
                const newSrc = pdf.src.split('?')[0] + `?t=${Date.now()}`; // Añadir un timestamp para evitar caché
                pdf.src = newSrc;
            } else {
                console.error('Error al generar el PDF:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    lastUpdateTimestamp = Date.now();

}

let lastUpdateTimestamp = Date.now();

function updateValue(id, value) {
    document.getElementById(`${id}-value`).innerText = value + (!['amount', 'cols', 'rows'].includes(id) ? " mm" : " ");

    const currentTimestamp = Date.now();

    if (lastUpdateTimestamp && (currentTimestamp - lastUpdateTimestamp > 5000)) {
        lastUpdateTimestamp = currentTimestamp;

        setTimeout(submitForm, 1000);
    }
}
