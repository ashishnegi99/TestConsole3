class TableHeader extends React.Component {
  render() {
    var classVal = "fa fa-refresh";
    if(this.props.fetching) {
      classVal = "fa fa-refresh" + " fa-spin";
    }

    return (
      <thead className="table-head">
        <tr>
          <th className="table-header" onClick={ () => this.props.onClick() }>
            STB &nbsp;
            <i className={ classVal}  aria-hidden="true"></i>
          </th>
          <th className="table-header">Status</th>
          <th className="table-header">Unit Address</th>
          <th className="table-header">Environment</th>
        </tr>
      </thead>
    );
  }
}

class TableRow extends React.Component {
  render() {
    var classVal = "fa fa-circle pull-right";
    var st = parseInt(this.props.value.STBStatus, 10);
    switch(st) {
      case 1:
            classVal += " available";
            break;
      case 2:
            classVal += " busy";
            break;
      case 0:
            classVal += " offline";
            break;
    }
    return (
      <tr key={i} className="stb-row">
        <td className="">
          <input type="checkbox" name="check1" value={this.props.value.STBLabel} onChange={ (event) => this.props.onClick(this.props.value.STBLabel, event) }/> 
          <span> {this.props.value.STBLabel} </span>
        </td>
        <td>
          <i className= {classVal} aria-hidden="true"></i>
        </td>
        <td>
          {this.props.value.UnitAdd}
        </td>
        <td>
          {this.props.value.Env}
        </td>
      </tr>
    );
  }
}

class Table extends React.Component {
  constructor() {
    super();
    this.state = {
      rows: [],
      fetching: true,
    }

  }

  componentDidMount() {
    this.handleRefresh();  
  }
  
  handleRefresh() {
    this.setState({ fetching: true });
    
    axios.get(window.config.stbStatusUrl)
    .then( res => {
      const rows = res.data;
      this.setState({
        rows: rows,
        fetching: false,
      });
    });
  }

  handleCheck(stbName) {
    if (window.runRevoJson.stbs.contains(stbName)) {
      window.runRevoJson.stbs.remove(stbName);
    } else {
      window.runRevoJson.stbs.push(stbName);
    }
  }

  renderRow(resp, i) {
    return (      
        <TableRow key={i} value={ resp[i] } onClick={ (stbName) => this.handleCheck(stbName) } />
    );
  }

  render() {
    var rows = [];
    for (var i=0; i < this.state.rows.length; i++) {
        rows.push(this.renderRow(this.state.rows,i));
    }
    return (
        <table id="example" className="table-class display nowrap dataTable no-footer collapsed">
          <TableHeader onClick={ () => this.handleRefresh() }  fetching= { this.state.fetching }/>
          <tbody id="stb-body">
            {rows}
          </tbody>
        </table>
    );
  }
}

ReactDOM.render(<Table/>, document.getElementById("stb-table"));