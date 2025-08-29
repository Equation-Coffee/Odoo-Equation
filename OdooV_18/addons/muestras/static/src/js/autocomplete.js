/** @odoo-module */

import { registry } from '@web/core/registry';
import { CharField } from '@web/views/fields/char/char_field';

export class AutocompleteContact extends CharField{
    setup(){
        super.setup();
        this.suggestions = [];
    }

    async onInput(event){
        super.onInput?.(event);
        const value = event.target.value;
        console.log("Input_value",value)
        if (value && value.length >=2){
            try{
                this.suggestions = await this.env.services.orm.searchRead(
                    "res.partner",
                    [["name", "ilike", value]],
                    ["name"],
                    { limit: 5 }
                );
                console.log()
                this.el.title = this.suggestions.map(r=> r.name).join(" | ") || "";
            } catch (error){    
                console.error("Error fetching suggestion:",error);
            }   
        } else {
            this.el.title = "";
        }
    }
    
    _renderReadOnly(){
        super._renderReadOnly();
        this.el.title="";
    }
}

registry.category("fields").add("muestras_autocomplete",AutocompleteContact);