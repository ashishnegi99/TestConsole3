class JRow extends React.Component {
  showConsole(value) {
    window.showConsole(value.jobNum, value.buildNum, value.suiteName);
  }

  stopJob(value) {
    var that = this;
    var config = {
      headers: {"X-CSRFToken": window.getCookie('csrftoken') }
    };

    axios.post(window.config.stopJob, { job: value.jobNum, build: value.buildNum }, config)
    .then(function(response) {
      that.props.handleRefresh();
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

    var form_val = this.props.value.jobNum + "," + this.props.value.buildNum;
    return (
      <tr>
          <td className={tdClass}>
            <input disabled={status} type="checkbox" value={form_val} name="builds" checked={ this.props.value.checked } onChange={() => this.props.onChange(this.props.index) }/> 
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
    this.state = {
      initialRows: [],
      rows: [],
      fetching: true,
      fields: this.getField()
    };
  }

  getField() {
    return {
      "jobNum"    : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '80px'
                      }
                    },
      "suiteName" : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '120px'
                      }
                    },
      "buildNum"  : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '80px'
                      }
                    }, 
      "result"    : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '80px'
                      }
                    },
      "startTime" : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '140px'
                      }
                    }, 
      "endTime"   : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '140px'
                      }
                    },
      "duration"  : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '90px'
                      }
                    }, 
      "userName"  : { "sorting" : 'none',
                      "filterText" : "",
                      "style" : {
                        width : '90px'
                      }
                    }
    };
  }

  componentDidMount() {
    this.handleRefresh();
  }
  
  handleRefresh() {
    this.setState ({
      initialRows: [],
      rows: [],
      fetching: true,
      fields: this.getField()
    });

    axios.get(window.config.jobStatusUrl)
    .then( res => {
      for (var i=0; i < res.data.length; i++) {
        res.data[i]['checked'] = false;
      }
      const rows = res.data.slice();

      this.setState({
        initialRows: rows,
        rows: rows,
        fetching: false,
        showFilter: false
      });
    });
  }

  onChange(i) {
    const newData = React.addons.update(this.state.rows, {
                    [i] : { 'checked' : {$set: !this.state.rows[i]['checked']}}
                  });
    this.setState({
      rows: newData
    });
  }

  renderRow(i) {
    return (      
        <JRow key={i} value={ this.state.rows[i]} onChange={(i) => this.onChange(i) }  fields={this.state.fields} index={i} handleRefresh={ this.handleRefresh.bind(this)}/>
    );
  }

  checkAll(e) {
    var rows = this.state.rows.slice();

    for (var i=0; i < rows.length; i++) {
      if(rows[i].result == "IN PROGRESS" || rows[i].result == "IN QUEUE") {
        rows[i]['checked'] = e.target.checked;
      }
    }
    this.setState( {
      rows : rows
    })
  }

  sortData(type, field) {
    var rows = this.state.rows.slice();
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

    this.setState( {
      rows : rows,
      fields: fields
    }) 
  }

  handleFilter(evt) {
    if(this._timeout){
        clearTimeout(this._timeout);
    }
    const val = evt.target.value;
    const field = evt.target.name;

    this._timeout = setTimeout( ()=>{
       this._timeout = null;
       this.filterObjets(field, val);
    },500);
  }

  filterObjets(field, val) {
    const newField = React.addons.update(this.state.fields, { [field] :  { "filterText" : { $set: val }}});
    var newData = this.state.initialRows.slice();

    newData = newData.filter(function(value) {
      
      if( (value['jobNum'].toLowerCase().indexOf(newField['jobNum']['filterText'].toLowerCase()) != -1)
          && (value['suiteName'].toLowerCase().indexOf(newField['suiteName']['filterText'].toLowerCase()) != -1)
          && (value['buildNum'].toLowerCase().indexOf(newField['buildNum']['filterText'].toLowerCase()) != -1)
          && (value['userName'].toLowerCase().indexOf(newField['userName']['filterText'].toLowerCase()) != -1 )) {
            return true;
      } else {
        return false;
      }
    });

    this.setState( {
      rows : newData,
      fields: newField
    });     
  }

  toggleFilter() {
    this.setState( {
      showFilter : !this.state.showFilter,
    });
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
    
    var filterCell = "hidden";
    if(this.state.showFilter) {
      filterCell = "";
    };

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
                <i className={ classVal}  aria-hidden="true" onClick={this.handleRefresh.bind(this)} ></i>
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
              <th className="quotation-mark" style={{ 'width' : '10px' }}>
                <i className="fa fa-filter filter-icon" aria-hidden="true" onClick={this.toggleFilter.bind(this)}></i>
              </th>
          </tr>
          <tr className={ filterCell }>
              <th className="quotation-mark fixed-width"></th>
              <th className="quotation-mark" style={this.state.fields["jobNum"]['style']}>
                <input type="text" style={{ 'width' : '80%'}} name="jobNum" onChange={this.handleFilter.bind(this)}/>
              </th>
              <th className="quotation-mark " style={this.state.fields["suiteName"]['style']}>
                <input type="text" style={{ 'width' : '80%'}} name="suiteName" onChange={this.handleFilter.bind(this)}/>
              </th>
              <th className="quotation-mark" style={this.state.fields["buildNum"]['style']}>
                <input type="text" style={{ 'width' : '80%'}} name="buildNum" onChange={this.handleFilter.bind(this)} />
              </th>
              <th className="quotation-mark" style={this.state.fields["result"]['style']}></th>
              <th className="quotation-mark" style={this.state.fields["startTime"]['style']}></th>
              <th className="quotation-mark" style={this.state.fields["endTime"]['style']}></th>
              <th className="quotation-mark" style={this.state.fields["duration"]['style']}></th>
              <th className="quotation-mark" style={this.state.fields["userName"]['style']}>
                  <input type="text" style={{ 'width' : '80%'}} name="userName" onChange={this.handleFilter.bind(this)} />
              </th>
              <th className="quotation-mark" style={{ 'width' : '80px' }}></th>
              <th className="quotation-mark" style={{ 'width' : '70px' }}></th>
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