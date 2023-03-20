window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
    const datatablesSimple2 = document.getElementById('datatablesSimple2');
    if (datatablesSimple2) {
        new simpleDatatables.DataTable(datatablesSimple2);
    }
    const datatablesSimplealimentos = document.getElementById('datatablesSimplealimentos');
    if (datatablesSimplealimentos) {
        new simpleDatatables.DataTable(datatablesSimplealimentos);
    }
    const datatablesSimplemedicamentos = document.getElementById('datatablesSimplemedicamentos');
    if (datatablesSimplemedicamentos) {
        new simpleDatatables.DataTable(datatablesSimplemedicamentos);
    }
    const datatablesSimpleaseo = document.getElementById('datatablesSimpleaseo');
    if (datatablesSimpleaseo) {
        new simpleDatatables.DataTable(datatablesSimpleaseo);
    }
    const datatablesSimplevacunas = document.getElementById('datatablesSimplevacunas');
    if (datatablesSimplevacunas) {
        new simpleDatatables.DataTable(datatablesSimplevacunas);
    }
    const datatablesSimpleaccesorios = document.getElementById('datatablesSimpleaccesorios');
    if (datatablesSimpleaccesorios) {
        new simpleDatatables.DataTable(datatablesSimpleaccesorios);
    }
    const datatablesSimplejuguetes = document.getElementById('datatablesSimplejuguetes');
    if (datatablesSimplejuguetes) {
        new simpleDatatables.DataTable(datatablesSimplejuguetes);
    }
});
