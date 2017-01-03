function TableHeader (props) {
  return (
    <thead>
      <tr>
        <th > &nbsp; STB</th>
        <th >SUITE NAME</th>
        <th >BUILD#</th>
        <th >RESULT</th>
        <th >JOB START TIME</th>
        <th >JOB END TIME</th>
        <th >DURATION</th>
        <th >TESTER</th>
        <th >STOP JOB</th>
      </tr>
    </thead>
  );
}

class Table extends React.Component {
  render() {
    return (
        <table id="example" className="display nowrap">
          <TableHeader/>
          <tbody id="testdataid"/>
        </table>
    );
  }
}

ReactDOM.render(<Table/>, document.getElementById("container"));