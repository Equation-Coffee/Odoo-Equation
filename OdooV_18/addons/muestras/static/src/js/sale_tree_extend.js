/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';

export class SaleListController extends ListController {
   setup() {
       super.setup();
   }
   OnTestClick() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'muestras.offering_pdf_wizard',
          name:'Open Wizard',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
registry.category("views").add("button_in_list", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_sale.ListView.Buttons",
});

class AtlasController extends ListController{
   async onBackendMethodClick(){
      try{
         const result = await this.env.services.orm.call('muestras.prueba','atlas',[],{});
         this.env.services.notification.add(result.mensaje || "Accion ejecutada",{type:'success'});
      } catch (error){
         this.env.services.notification.add("Error en la ejecución del método" + error.message,{type:'danger'});
         console.error(error)
      }
   }  
}

registry.category("views").add("button_atlas_update",{
   ...listView,
   Controller: AtlasController,
   buttonTemplate: "button_sale.atlas_update"
})