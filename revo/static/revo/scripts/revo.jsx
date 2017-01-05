
function TableHeader(props) {
  return (
    <thead className="table-head">
      <tr>
        <th className="table-header">STB</th>
        <th className="table-header">Status</th>
        <th className="table-header">Unit Address</th>
        <th className="table-header">Environment</th>
      </tr>
    </thead>
  );
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
          <input type="checkbox" name="check1" value={this.props.value.STBLabel} /> 
          <span> {this.props.value.STBLabel} </span>
        </td>
        <td>
          <i className= {classVal} aria-hidden="true"></i>
        </td>
        <td>
          {this.props.value.STBSno}
        </td>
        <td>
          {this.props.value.RouterSNo}
        </td>
      </tr>
    );
  }
}

class Table extends React.Component {
  renderRow(resp, i) {
    return (      
        <TableRow key={i} value={ resp[i] } />
    );
  }

  render() {
    var rows = [];
    var resp = [
      {"STBStatus": "1", "RouterSNo": "R1", "STBLabel": "STB 1", "STBSno": "M11435TDS144"},
      {"STBStatus": "1", "RouterSNo": "R1", "STBLabel": "STB 2", "STBSno": "M11543TH4292"},
      {"STBStatus": "2", "RouterSNo": "R1", "STBLabel": "STB 3", "STBSno": "SN005"},
      {"STBStatus": "1", "RouterSNo": "R1", "STBLabel": "STB 4", "STBSno": "M11509TD9937"},
      {"STBStatus": "1", "RouterSNo": "R1", "STBLabel": "STB 5", "STBSno": "M11543TH4258"},
      {"STBStatus": "1", "RouterSNo": "R1", "STBLabel": "STB 6", "STBSno": "SN005"},
      {"STBStatus": "0", "RouterSNo": "R1", "STBLabel": "STB 7", "STBSno": "SN006"},
      {"STBStatus": "0", "RouterSNo": "R1", "STBLabel": "STB 8", "STBSno": "SN007"}
    ];
    for (var i=0; i < resp.length; i++) {
        rows.push(this.renderRow(resp,i));
    }

    return (
        <table id="example" className="table-class display nowrap dataTable no-footer collapsed">
          <TableHeader/>
          <tbody id="stb-body">
            {rows}
          </tbody>
        </table>
    );
  }
}

ReactDOM.render(<Table/>, document.getElementById("stb-table"));