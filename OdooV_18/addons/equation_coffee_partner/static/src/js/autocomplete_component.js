import { AutoComplete } from "@web/core/autocomplete/autocomplete";

export class EquationCoffeeContactAutoComplete extends AutoComplete {
    static template = 'equation_coffee.ContactAutoComplete';

    setup(){
        super.setup();
        console.log("✅ equation_coffee.ContactAutComplete cargado correctamente");
        this.localValue = "";
        
        
        // 🔹 Opciones iniciales "mock" (solo para ver que aparece el dropdown)
        // this.state.options = [
        //      { id: 1, name: "Juan Pérez", description: "Cliente Bogotá" },
        //      { id: 2, name: "María Gómez", description: "Cliente Medellín" },
        //      { id: 3, name: "Café Ltda.", description: "Empresa exportadora" },
        //  ];
        // this.state.open = true; // 🔹 Forzamos a que se vea
    }       

       
    onInput(ev) {
        this.localValue = ev.target.value;  // solo actualizar local
        if (this.localValue.length > 2) {
            const optionsSource = this.props.sources?.[0]?.options;
            if (typeof optionsSource === "function") {
                optionsSource(this.localValue).then(results => {
                    this.state.options = (results || []).slice(0, 3);     // ← solo 3
                    this.state.open = this.state.options.length > 0; 
                    this.render(true);                                    // ← repintar
                });
            }
        } else {
            this.state.options = [];
            this.state.open = false;
            this.render(true);                                            // ← repintar
        }
    }


    // onInput(ev) {

    //     const value = ev.target.value;

    //     // 🔹 Actualiza solo el valor del input
    //     if (this.props.onChange) {
    //         this.props.onChange(value);
    //     }

    //     // 🔹 Si es muy corto, no mostrar nada
    //     if (!value || value.length <= 2) {
    //         this.state.options = [];
    //         this.state.open = false;
    //         return;
    //     }

    //     // 🔹 Obtener sugerencias sin modificar el input
    //     const optionsSource = this.props.sources?.[0]?.options;
    //     if (typeof optionsSource === "function") {
    //         optionsSource(value).then(results => {
    //             this.state.options = results; // Solo para el dropdown
    //             this.state.open = results.length > 0;
    //         });
    //     }
    // }
    // onInput(ev) {
    //     const value = ev.target.value;
    //     this.localValue = value; // actualizar solo local

    //     // Opcional: actualizar el dropdown
    //     const optionsSource = this.props.sources?.[0]?.options;
    //     if (typeof optionsSource === "function" && value.length > 2) {
    //         optionsSource(value).then(results => {
    //             this.state.options = results;
    //             this.state.open = results.length > 0;
    //         });
    //     } else {
    //         this.state.options = [];
    //         this.state.open = false;
    //     }
    // }







    onKeyDown(ev) {
        // Opcional: manejar flechas, enter, etc.
        if (ev.key === "Enter") {
            console.log("Enter presionado, valor:", ev.target.value);
        }
    }

//     loadOptions(options, request) {
//     console.debug("Autocomplete request:", request);
//     if (typeof options === "function") {
//         return options(request);
//     } else {
//         return options; 
//     }
// }

} 


