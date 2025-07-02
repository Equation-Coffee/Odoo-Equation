/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";

class CustomTreeButtonController extends ListController {
    setup() {
        super.setup();
    }

    onCustomButtonClick() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Ejemplo",
            res_model: "tu.modelo",
            view_mode: "form",
            target: "new",
        });
    }
}

registry.category("controllers").add("custom_tree_button", CustomTreeButtonController);

// registry.category("views").add("custom_tree_button", {
//     viewType: "list",
//     Controller: CustomTreeButtonController,
// });
