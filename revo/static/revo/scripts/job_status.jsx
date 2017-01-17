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
          <td style={this.props.fields["jobNum"]['style']}>
            <span> {this.props.value["jobNum"]} </span>
          </td>
          <td className="filterable-cell"  style={this.props.fields["suiteName"]['style']}>{this.props.value["suiteName"]} </td>
          <td className="filterable-cell"  style={this.props.fields["buildNum"]['style']}>{this.props.value["buildNum"]} </td>
          <td className={resultclass}  style={this.props.fields["result"]['style']} >{this.props.value.result} </td>
          <td className="filterable-cell"  style={this.props.fields["startTime"]['style']}>{this.props.value.startTime} </td>
          <td className="filterable-cell"  style={this.props.fields["endTime"]['style']}>{this.props.value.endTime} </td>
          <td className="filterable-cell"  style={this.props.fields["duration"]['style']}>{this.props.value.duration} </td>
          <td className="filterable-cell"  style={this.props.fields["userName"]['style']}>{this.props.value.userName} </td>
          <td className="filterable-cell"  style={{ 'width' : '80px' }}>
            <button type="button" className="btn btn-danger" disabled={status} onClick={() => this.stopJob(this.props.value)} > STOP </button>
          </td>
          <td className="filterable-cell"  style={{ 'width' : '70px' }}>
            <a href="#" onClick={() => this.showConsole(this.props.value)} className={linkclass} >Console</a>
          </td>
      </tr>
    )
  }
}

class JTable extends React.Component {
  constructor() {
    super();

    const fields = {
      "jobNum"    : { "sorting" : 'none',
                      "style" : {
                        width : '80px'
                      }
                    },
      "suiteName" : { "sorting" : 'none',
                      "style" : {
                        width : '120px'
                      }
                    },
      "buildNum"  : { "sorting" : 'none',
                      "style" : {
                        width : '80px'
                      }
                    }, 
      "result"    : { "sorting" : 'none',
                      "style" : {
                        width : '80px'
                      }
                    },
      "startTime" : { "sorting" : 'none',
                      "style" : {
                        width : '140px'
                      }
                    }, 
      "endTime"   : { "sorting" : 'none',
                      "style" : {
                        width : '140px'
                      }
                    },
      "duration"  : { "sorting" : 'none',
                      "style" : {
                        width : '90px'
                      }
                    }, 
      "userName"  : { "sorting" : 'none',
                      "style" : {
                        width : '90px'
                      }
                    }
    };

    this.state = {
      rows: [],
      fetching: true,
      fields: fields
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
        <JRow key={i} value={ this.state.rows[i]} onChange={(i) => this.onChange(i) }  fields={this.state.fields } />
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

  sortData(type, field) {
    var rows = this.state.rows;
    var fields = this.state.fields;
    var asc = true;
    if(fields[field]['sorting'] === 'asc') {
      asc = false; 
      fields[field]['sorting'] = 'des';
    } else {
      asc = true;
      fields[field]['sorting'] = 'asc';
    }

    rows.sort(function(a,b) {
      if(type === "String") {
        return asc ? a[field].localeCompare(b[field]) : b[field].localeCompare(a[field]);
      } else if(type === "Int") {
        return asc ? parseFloat(a[field]) - parseFloat(b[field]) : parseFloat(b[field]) - parseFloat(a[field]);
      } else if(type === "Time") {
        if(a[field] === "...") {
          return asc ? -1 : 1;
        }
        if(b[field] === "...") {
          return asc ? 1 : -1;
        }
        return asc ? Date.parse(b[field]) - Date.parse(a[field]) : Date.parse(a[field]) - Date.parse(b[field]);
      }
    });

    const newData = rows;
    this.setState( {
      rows : newData,
      fields: fields
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
              <th className="quotation-mark" style={this.state.fields["jobNum"]['style']}>
                <i className="fa fa-sort" aria-hidden="true" onClick={() => this.sortData('String','jobNum')}></i>
                  STB &nbsp;
                <i className={ classVal}  aria-hidden="true"></i>
              </th>
              <th className="quotation-mark " style={this.state.fields["suiteName"]['style']}>SUITE NAME
                  <i className="fa fa-sort" aria-hidden="true" onClick={() => this.sortData('String','suiteName')}></i>
              </th>
              <th className="quotation-mark" style={this.state.fields["buildNum"]['style']}>BUILD#</th>
              <th className="quotation-mark" style={this.state.fields["result"]['style']}>RESULT
                <i className="fa fa-sort" aria-hidden="true" onClick={() => this.sortData('String','result')}></i>
              </th>
              <th className="quotation-mark" style={this.state.fields["startTime"]['style']}>START TIME
                <i className="fa fa-sort" aria-hidden="true" onClick={() => this.sortData('Time','startTime')}></i>
              </th>
              <th className="quotation-mark" style={this.state.fields["endTime"]['style']}>END TIME
                <i className="fa fa-sort" aria-hidden="true" onClick={() => this.sortData('Time','endTime')}></i>
              </th>
              <th className="quotation-mark" style={this.state.fields["duration"]['style']}>DURATION</th>
              <th className="quotation-mark" style={this.state.fields["userName"]['style']}>TESTER
                <i className="fa fa-sort" aria-hidden="true" onClick={() => this.sortData('String','userName')}></i>
              </th>
              <th className="quotation-mark" style={{ 'width' : '80px' }}>STOP</th>
              <th className="quotation-mark" style={{ 'width' : '70px' }}>OUTPUT</th>
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