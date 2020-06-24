import React, {Component} from "react";
import ObjetosDeGastosService from "../../services/ObjetosDeGastos"
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import DataTable from "react-data-table-component";
import SimpleEdit from "../Forms/SimpleEdit";
import NuevoObjetoDeGasto from "../Forms/NuevoObjetoDeGasto";
import Popups from "../Popups";

class ObjetoDeGasto extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      totalRows: 0,
      objetosDeGastos: [],
      objetoDeGasto: {
        id: 0,
        descripcion: '',
        activo: true
      }
    };
    this.retrieveObjetosDeGastos = this.retrieveObjetosDeGastos.bind(this);
    this.getObjectRow = this.getObjectRow.bind(this);
    this.saveModalEdit = this.saveModalEdit.bind(this);
    this.saveModalNew = this.saveModalNew.bind(this);
    this.handleOnclickDelete = this.handleOnclickDelete.bind(this);
  }

  getObjectRow = row => {
    ObjetosDeGastosService.getById(row.id).then(response => {
      this.setState({
        objetoDeGasto: response.data
      })
    });
  }

  handleOnclickDelete = row => {
    let tempObjetosDeGastos = this.state.objetosDeGastos;
    let indexOfId = tempObjetosDeGastos.findIndex(e => e.id === row.id);
    if (indexOfId > -1) {
      ObjetosDeGastosService.delete(row.id)
        .then(response => {
          if (response.status === 204) {
            tempObjetosDeGastos.splice(indexOfId, 1);
            this.setState({objetosDeGastos: tempObjetosDeGastos});
            Popups.success("Eliminado con éxito");
          } else {
            Popups.error("Ocurrió un error, no se pudo eliminar");
          }
        })
        .catch(e => {
          console.log(e);
        });
    } else {
      Popups.error("No se encontró el objeto de gasto");
    }
  }

  saveModalNew(data) {
    let tempObjetosDeGastos = this.state.objetosDeGastos;
    let objDeGasto = {
      id: data.id,
      descripcion: data.descripcion,
      activo: data.activo ? "Activo" : "Inactivo"
    };
    tempObjetosDeGastos.push(objDeGasto);
    this.setState({objetosDeGastos: tempObjetosDeGastos});
  }

  saveModalEdit(data) {
    let tempObjetosDeGastos = this.state.objetosDeGastos;
    let indexOfId = tempObjetosDeGastos.findIndex(e => e.id === data.id);
    if (indexOfId > -1) {
      tempObjetosDeGastos[indexOfId] = {
        id: data.id,
        descripcion: data.descripcion,
        activo: data.activo ? "Activo" : "Inactivo"
      };
      this.setState({objetosDeGastos: tempObjetosDeGastos});
    }

  }

  retrieveObjetosDeGastos(page) {
    this.setState({loading: true});
    ObjetosDeGastosService.getAll(page)
      .then(response => {
        this.setState({
          objetosDeGastos: response.data.results.map(odg => {
            return {
              id: odg.id,
              descripcion: odg.descripcion,
              activo: odg.activo ? "Activo" : "Inactivo"
            }
          }),
          loading: false
        });
      })
      .catch(e => {
        console.log(e);
      })
  }

  handlePageChange = async page => {
    this.retrieveObjetosDeGastos(page);
  }

  componentDidMount() {
    this.retrieveObjetosDeGastos("1");
  }

  render() {
    let columns = [
      {
        name: 'Descripción',
        selector: 'descripcion',
        sortable: true,
        
      },
      {
        name: 'Activo',
        selector: 'activo',
        sortable: true,
      },
      {
        name: 'Acciones',
        cell: row =>
          <div>
            <button
              className="btn btn-sm btn-link text-primary" data-toggle="modal" data-target="#editModal"
              onClick={() => this.getObjectRow(row)}>
              <FontAwesomeIcon icon="edit"/>
            </button>
            <button
              className="btn btn-sm btn-link text-danger" onClick={() => {
              if (window.confirm('Estás seguro de eliminar?')) {
                this.handleOnclickDelete(row)
              }
            }}>
              <FontAwesomeIcon icon="trash-alt"/>
            </button>
          </div>,
        button: true,
      }
    ];
    const paginationOptions = {
      rowsPerPageText: 'Filas por página',
      rangeSeparatorText: 'de',
      selectAllRowsItem: true,
      selectAllRowsItemText: 'Todos'
    };

    return (
      <div>
        <div className="d-sm-flex align-items-center justify-content-between mb-4">
          <h1 className="h3 mb-0 text-gray-800">Objetos de Gastos</h1>
          <button className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm" data-toggle="modal"
                  data-target="#newModal"><FontAwesomeIcon icon="plus" size="sm"
                                                           className="text-white-50"/>&nbsp;Nuevo
          </button>
        </div>
        <div>
          <DataTable
            columns={columns}
            data={this.state.objetosDeGastos}
            defaultSortField="descripcion"
            progressPending={this.state.loading}
            pagination
            paginationServer
            onChangePage={this.handlePageChange}
            paginationComponentOptions={paginationOptions}
            highlightOnHover={true}
            noHeader={true}
            dense={true}
            className="table table-sm table-bordered"
          />

          {/*Modal de nuevo objeto de gasto*/}
          <NuevoObjetoDeGasto
            saveModalNew={this.saveModalNew}
          />

          {/*Modal de nuevo objeto de gasto*/}
          <SimpleEdit
            title="Objeto de gasto"
            item={this.state.objetoDeGasto}
            saveModalEdit={this.saveModalEdit}
            service={ObjetosDeGastosService}
          />
        </div>
      </div>
    );
  }
}

export default ObjetoDeGasto;