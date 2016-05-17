/**
 * Created by bulos87 on 5/12/16.
 */

//*******************************************************************
//  CREATE MATRIX AND MAP
//*******************************************************************
function draw_chord_graph(date_string) {

    var json_file = 'hour_files/'+date_string+'_matrix_ratios.json';
    var matrix_file = 'hour_files/'+date_string+'_catalogue.csv';

    queue()
        .defer(d3.json, json_file)
        .defer(d3.csv, matrix_file)
        .await(function (err, matrix, mmap) {
            if (err) console.log(err);
            _.each(mmap, function (d, i) {
                d.id = i;
                d.data = d.color
            });
            drawChords(matrix, mmap);
        });
    //*******************************************************************
    //  DRAW THE CHORD DIAGRAM
    //*******************************************************************
    function drawChords(matrix, mmap) {
        var w = 980, h = 800, r1 = h / 2, r0 = r1 - 110;

        var chord = d3.layout.chord()
            .padding(.02)
            .sortSubgroups(d3.descending)
            .sortChords(d3.descending);

        var arc = d3.svg.arc()
            .innerRadius(r0)
            .outerRadius(r0 + 20);

        var svg = d3.select("div#chords_container")
            .append("svg:svg")
            .attr("width", w)
            .attr("height", h)
            .append("svg:g")
            .attr("id", "circle")
            .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

        svg.append("circle")
            .attr("r", r0 + 20);

        var rdr = chordRdr(matrix, mmap);
        chord.matrix(matrix);

        var g = svg.selectAll("g.group")
            .data(chord.groups())
            .enter().append("svg:g")
            .attr("class", "group")
            .on("mouseover", mouseover)
            .on("mouseout", function (d) {
                d3.select("#tooltip").style("visibility", "hidden")
            });

        g.append("svg:path")
            .style("stroke", "grey")
            .style("fill", function (d) {
                return rdr(d).gdata;
            })
            .attr("d", arc);

        g.append("svg:text")
            .each(function (d) {
                d.angle = (d.startAngle + d.endAngle) / 2;
            })
            .attr("dy", ".35em")
            .style("font-family", "helvetica, arial, sans-serif")
            .style("font-size", "9px")
            .attr("text-anchor", function (d) {
                return d.angle > Math.PI ? "end" : null;
            })
            .attr("transform", function (d) {
                return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
                    + "translate(" + (r0 + 26) + ")"
                    + (d.angle > Math.PI ? "rotate(180)" : "");
            })
            .text(function (d) {
                return rdr(d).gname;
            });

        var chordPaths = svg.selectAll("path.chord")
            .data(chord.chords())
            .enter().append("svg:path")
            .attr("class", "chord")
            .style("stroke", "grey")
            .style("fill", function (d) {
                return _.where(mmap, {id: d.source.index})[0].data;
            })
            .attr("d", d3.svg.chord().radius(r0))
            .on("mouseover", function (d) {
                d3.select("#tooltip")
                    .style("visibility", "visible")
                    .html(chordTip(rdr(d)))
                    .style("top", function () {
                        return (d3.event.pageY - 100) + "px"
                    })
                    .style("left", function () {
                        return (d3.event.pageX - 100) + "px";
                    })
            })
            .on("mouseout", function (d) {
                d3.select("#tooltip").style("visibility", "hidden")
            });

        function chordTip(d) {
            var p = d3.format(".1%"), q = d3.format(",.2r");
            return "Chord Info:<br/>"
                + d.sname + " → " + d.tname
                + ": " + p(d.svalue) + "<br/>"
                + d.tname + " → " + d.sname
                + ": " + p(d.tvalue) + "<br/>";
        }

        function groupTip(d) {
            var p = d3.format(".1%"), q = d3.format(",.2r");
            return "Trips Info:<br/>"
                + d.gname + " : " + p(d.gvalue) + "<br/>";
        }

        function mouseover(d, i) {
            d3.select("#tooltip")
                .style("visibility", "visible")
                .html(groupTip(rdr(d)))
                .style("top", function () {
                    return (d3.event.pageY - 80) + "px"
                })
                .style("left", function () {
                    return (d3.event.pageX - 130) + "px";
                });

            chordPaths.classed("fade", function (p) {
                return p.source.index != i
                    && p.target.index != i;
            });
        }
    }
}
