/** @odoo-module **/

import { registry } from '@web/core/registry';
import { CharField,charField } from '@web/views/fields/char/char_field';

import xmlTemplate from 'equation_coffee_partner/static/src/xml/simple_autocomplete_char.xml';

export class SimpleAutocompleteChar extends CharField {
    static template = 'equation_coffee_partner.SimpleAutocompleteChar';
    setup() {
        super.setup();
        console.log("✅ contact_autocomplete cargado correctamente");
        this.suggestions = [];
        this.el.addEventListener('input', this.onInput.bind(this));
    }

    async onInput(event) {
        super.onInput?.(event);
        console.log("Input detectado:", event.target.value);
        const value = event.target.value;

        if (value && value.length >= 2) {
            try {
                this.suggestions = await this.env.services.orm.searchRead(
                    'res.partner',
                    [['name', 'ilike', value]],
                    ['name'],
                    { limit: 5 }
                );
                this.el.title = this.suggestions.map(r => r.name).join(' | ') || '';
            } catch (error) {
                console.error('Error fetching suggestions:', error);
            }
        } else {
            this.el.title = '';
        }
    }

    _renderReadOnly() {
        super._renderReadOnly();
        this.el.title = '';
    }
}

registry.category("fields").add("simple_autocomplete_char", {
    ...charField,
    component: SimpleAutocompleteChar,
});
