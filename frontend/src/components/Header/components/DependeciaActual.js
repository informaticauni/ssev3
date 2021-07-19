import React, { Component } from "react";
import DependenciasPorUsuarioService from "../../../services/DependenciasPorUsuario";
import helper from "../../../utils/helper";

class DependenciaActual extends Component {
    constructor(props) {
        super(props);
        this.state = {
            dependecias: []
        }
    }

    componentDidMount() {
        this.retrieveDependenciasByUser();
      }
    /**
   * Obtener las posibles dependencias de origen de acuerdo al usuario activo.
   */
    retrieveDependenciasByUser() {
        if (helper.getCurrentUserId() !== undefined) {
            DependenciasPorUsuarioService.getByUser(helper.getCurrentUserId())
                .then(response => {
                    this.setState({
                        dependecias: response.data.map(dxu => {
                            return dxu.dependencia_id.descripcion + ' '
                        })
                    })
                })
                .catch(e => {
                    console.log(`Error DependenciasPorUsuarioService.\n${e}`);
                });
        }
    }
    render() {
        return (
            <>
            {(sessionStorage.getItem('isAdmin') === 'false') ?
            <span>{this.state.dependecias} </span>:<div/>}
            </>
        )
    }



}
export default DependenciaActual;
