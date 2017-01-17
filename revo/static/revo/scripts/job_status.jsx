class JRow extends React.Component {
  showConsole(value) {
    window.showConsole(value.jobNum, value.buildNum, value.suiteName);
  }

  stopJob(value) {
    axios.post(window.config.stopJob, { job: value.jobNum, build: value.buildNum })
    .then(function(response) {
    });
  }

  render() {
    var tdClass = "fixed-width", disabled = "", resultclass= "filterable-cell",  linkclass= "",  status= "";
    var item = this.props.value;

    if(item.result == "SUCCESS"){
      resultclass = " result_available";
      linkclass = "";
      status = "disabled";
      tdClass += " half_opaque";
    }
    else if(item.result == "FAILURE"){
      resultclass = " result_offline";
      linkclass = "";
      status = 'disabled';
      tdClass += " half_opaque";
    }
    else if(item.result == "IN PROGRESS"){
      resultclass = " result_progress";
      linkclass = "";
      status = '';
    }
    else if(item.result == "IN QUEUE"){
      resultclass = " result_queue";
      linkclass = "not-active";
      status = '';
    }
    else if(item.result == "ABORTED"){
      resultclass = " result_aborted";
      linkclass = "not-active";
      status = 'disabled';
      tdClass += " half_opaque";
    }

    return (
      <tr>
          <td className={tdClass}>
            <input disabled={status} type="checkbox" name="stbs" checked={ this.props.value.checked } onChange={() => this.props.onChange(this.props.key) }/> 
          </td>
          <td>
            <span> {this.props.value["Job No"]} </span>
          </td>
          <td className="filterable-cell">{this.props.value["suiteName"]} </td>
          <td className="filterable-cell">{this.props.value["buildNum"]} </td>
          <td className={resultclass} >{this.props.value.result} </td>
          <td className="filterable-cell">{this.props.value.startTime} </td>
          <td className="filterable-cell">{this.props.value.endTime} </td>
          <td className="filterable-cell">{this.props.value.duration} </td>
          <td className="filterable-cell">{this.props.value.userName} </td>
          <td className="filterable-cell">
            <button type="button" className="btn btn-danger" disabled={status} onClick={() => this.stopJob(this.props.value)} > STOP </button>
          </td>
          <td className="filterable-cell">
            <a href="#" onClick={() => this.showConsole(this.props.value)} className={linkclass} >Console</a>
          </td>
      </tr>
    )
  }
}

class JTable extends React.Component {
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
    
    axios.get(window.config.jobStatusUrl)
    .then( res => {
      for (var i=0; i < res.data.length; i++) {
        res.data[i]['checked'] = false;
      }
      const rows = res.data;

      this.setState({
        rows: rows,
        fetching: false,
      });
    });
  }

  onChange(i) {
    const newData = update(this.state.rows, {
                    i : { 'checked' : {$set: !this.state.rows[i]['checked']}}
                  });
    this.setState({
      rows: newData
    });
  }

  renderRow(i) {
    return (      
        <JRow key={i} value={ this.state.rows[i]} onChange={(i) => this.onChange(i) } />
    );
  }

  checkAll() {
    var rows = this.state.rows;
    for (var i=0; i < rows.length; i++) {
      if(rows[i].result == "IN PROGRESS" || rows[i].result == "IN QUEUE") {
        rows[i]['checked'] = !rows[i]['checked'];
      }
    }
    const newData = rows;
    this.setState( {
      rows : newData
    })
  }

  render() {
    var rows = [];
    for (var i=0; i < this.state.rows.length; i++) {
        rows.push(this.renderRow(i));
    }

    var classVal = "fa fa-refresh";
    if(this.state.fetching) {
      classVal = "fa fa-refresh fa-spin";
    }
    
    return (
      <table className="react-table table table-striped">
        <thead>
          <tr>
              <th className="quotation-mark fixed-width">
                <input type="checkbox" name="chk[]" className="parent_chk_job" id="parent_chk_job" onChange={ this.checkAll.bind(this) }/>
              </th>
              <th className="quotation-mark">STB &nbsp;
                <i className={ classVal}  aria-hidden="true"></i>
              </th>
              <th className="quotation-mark">SUITE NAME</th>
              <th className="quotation-mark">BUILD#</th>
              <th className="quotation-mark">RESULT</th>
              <th className="quotation-mark">START TIME</th>
              <th className="quotation-mark">END TIME</th>
              <th className="quotation-mark">DURATION</th>
              <th className="quotation-mark">TESTER</th>
              <th className="quotation-mark">STOP</th>
              <th className="quotation-mark">OUTPUT</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
        
      </table>
    )
  }
}

ReactDOM.render(<JTable/>, document.getElementById("job-status-table"));