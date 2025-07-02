odoo.define('muestras.AutoSyncOnLoad', function (require) {
    'use strict';

    const ListController = require('web.ListController');
    const rpc = require('web.rpc');

    ListController.include({
        /**
         * Sobrecargamos el inicio de la vista
         */
        willStart: function () {
            if (this.modelName === 'muestras.prueba') { // Ajusta al modelo asociado
                console.log('Sincronizando datos al cargar la vista...');
                rpc.query({
                    model: 'muestras.modelo',
                    method: '_atlas', // Llamamos al método _atlas en el backend
                    args: [],
                }).then(function (result) {
                    console.log('Sincronización completada:', result);
                }).catch(function (error) {
                    console.error('Error durante la sincronización:', error);
                });
            }
            return this._super.apply(this, arguments);
        },
    });
});
