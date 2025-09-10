/** @odoo-module **/

import { CharField, charField } from '@web/views/fields/char/char_field';
import { registry } from "@web/core/registry";
import { useChildRef, useService } from '@web/core/utils/hooks';
import { useInputField } from "@web/views/fields/input_field_hook";
import { _t } from "@web/core/l10n/translation";
import { EquationCoffeeContactAutoComplete } from "./autocomplete_component";

export class EquationCoffeeContactAutoCompleteCharField extends CharField {
    static template = 'equation_coffee.ContactAutoCompleteCharField';
    static components = { ...CharField.components, EquationCoffeeContactAutoComplete };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.inputRef = useChildRef();

        // Fuente única del valor: record/props (NO estado local)
        const getPropValue = () =>
            (this.props.value ?? this.props.record?.data?.[this.props.name] ?? "");

        // Solo usamos localValue como "query" para el dropdown (no para pintar el input)
        this.localValue = getPropValue();

        useInputField({
            ref: this.inputRef,
            // 👇 Igual que el partner autocomplete: leer SIEMPRE del record/props
            getValue: () => getPropValue(),
            parse: (v) => (this.parse ? this.parse(v) : (v ?? "")),
            // Actualizamos solo la query para el dropdown (no tocamos el modelo aquí)
            onChange: (v) => { this.localValue = v ?? ""; },
        });
    }

    async validateSearchTeam(request) {
        return request && request.length > 2;
    }

    get sources() {
        return [
            {
                options: async (request = "") => {
                    if (request.length < 3) return [];
                    const contacts = await this.orm.searchRead(
                        "res.partner",
                        [["name", "ilike", request]],
                        ["id", "name", "email"]
                    );
                    return contacts.map(c => ({
                        id: c.id,
                        name: c.name,
                        description: c.email || "",
                    }));
                },
                placeholder: _t('Searching Existing Contacts'),
            },
        ];
    }

    onBlur() {
        if (this.props.readonly) return;
        // Guardamos lo que está en pantalla. Si no hubiera localValue, usamos el valor del record
        const getPropValue = () =>
            (this.props.value ?? this.props.record?.data?.[this.props.name] ?? "");
        const valueToSave = (this.localValue ?? "").toString();
        // Si quieres guardar solo en blur (no cada tecleo):
        this.props.onChange?.(valueToSave || getPropValue());
    }
    getQuery() {
    // lee lo que hay VISUALMENTE en el input si existe,
    // o cae al valor del record/props
    return this.inputRef?.el?.value
        ?? this.props.value
        ?? this.props.record?.data?.[this.props.name]
        ?? "";
    }
}

export const equationCoffeeContactAutoCompleteCharField = {
    ...charField,
    component: EquationCoffeeContactAutoCompleteCharField,
};

registry.category("fields").add(
    "equation_coffee_contact_autocomplete",
    equationCoffeeContactAutoCompleteCharField
);
