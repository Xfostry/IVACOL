// Función centralizada para cálculo de neto, iva y total según categoría y tipo de monto
function calcularIvaYTotales({ valor, tipoMonto = 'neto', categoria = '' }) {
    let neto = 0;
    let total = 0;
    let iva = 0;
    let ivaRate = 0.19;
    let ivaExcluido = false;
    const cat = (categoria || '').toLowerCase();
    if (["alimentos", "medicamentos", "servicios", "servicios públicos"].some(c => cat.includes(c))) {
        ivaRate = 0.05;
    } else if (["libros", "educación", "salud"].some(c => cat.includes(c))) {
        ivaRate = 0;
    } else if (["exportaciones", "donaciones", "operaciones financieras"].some(c => cat.includes(c))) {
        ivaRate = 0;
        ivaExcluido = true;
    }
    if (tipoMonto === 'total') {
        total = Number(valor) || 0;
        neto = ivaExcluido ? total : parseFloat((total / (1 + ivaRate)).toFixed(2));
        iva = ivaExcluido ? 0 : parseFloat((total - neto).toFixed(2));
    } else {
        neto = Number(valor) || 0;
        iva = ivaExcluido ? 0 : parseFloat((neto * ivaRate).toFixed(2));
        total = parseFloat((neto + iva).toFixed(2));
    }
    return { neto, iva, total };
}
