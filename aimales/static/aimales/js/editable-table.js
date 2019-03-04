var EditableTable = function () {

'use strict';

    return {
        init: function () {
            function restoreRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                    oTable.fnUpdate(aData[i], nRow, i, false);
                }
                oTable.fnDraw();
            }

            function editRow(oTable, nRow, is_new=false) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                // ID
                if(is_new){
                    var max_id = 1;
                    $("table tr td:first-child").each(function(i){
                        if(parseInt($(this).text()) > max_id){
                            max_id = parseInt($(this).text());
                        }
                    });
                    jqTds[0].innerHTML = '<input readonly="readonly" style="width:100%;" type="text" class="form-control small" value="' + (max_id + 1).toString() + '">';
                }else{
                    jqTds[0].innerHTML = '<input readonly="readonly" style="width:100%;" type="text" class="form-control small" value="' + aData[0] + '">';
                }
                // MD5
                jqTds[1].innerHTML = '<input readonly="readonly" style="width:100%;" type="text" class="form-control small" placeholder="自动计算" value="' + aData[1] + '">';
                // 负载内容
                jqTds[2].innerHTML = '<input style="width:100%;" type="text" class="form-control small" value="' + aData[2] + '">';
                // 分词结果
                jqTds[3].innerHTML = '<input style="width:100%;" type="text" class="form-control small" value="' + aData[3] + '">';
                // 标注结果
                jqTds[4].innerHTML = '<input style="width:100%;" type="text" class="form-control small" value="' + aData[3] + '">';
                // 时间戳
                jqTds[5].innerHTML = '<input style="width:100%;" type="text" class="form-control small" value="' + aData[3] + '">';
                // 编辑栏
                if(is_new){
                    jqTds[6].innerHTML = '<a class="save" data-mode="new" href=""><i class="fa fa-save">保存&emsp;</i></a> <a data-mode="new" class="cancel" href=""><i class="fa fa-undo">取消</i></a>';
                }else{
                    jqTds[6].innerHTML = '<a class="save" data-mode="old" href=""><i class="fa fa-save">保存&emsp;</i></a> <a data-mode="old" class="cancel" href=""><i class="fa fa-undo">取消;</i></a>';
                }
            }

            function saveRow(oTable, nRow) {
                console.log("call saveRow...");
                var jqInputs = $('input', nRow);
                oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
                // Md5根据负载自动计算
                var pcap_md5 = md5(jqInputs[2].value);
                console.log(pcap_md5);
                oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);
                oTable.fnUpdate(jqInputs[2].value, nRow, 2, false);
                oTable.fnUpdate(jqInputs[3].value, nRow, 3, false);
                oTable.fnUpdate(jqInputs[4].value, nRow, 4, false);
                oTable.fnUpdate(jqInputs[5].value, nRow, 5, false);
                oTable.fnUpdate('<a class="edit" href=""><i class="fa fa-save">编辑&emsp;</i></a> <a class="cancel" href=""><i class="fa fa-undo">取消;</i></a>', nRow, 6, false);
                oTable.fnDraw();
            }

            function cancelEditRow(oTable, nRow) {
                console.log("cancel saveRow...");
                var jqInputs = $('input', nRow);
                oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
                oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);
                oTable.fnUpdate(jqInputs[2].value, nRow, 2, false);
                oTable.fnUpdate(jqInputs[3].value, nRow, 3, false);
                oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 4, false);
                oTable.fnDraw();
            }
            var oTable = $('#editable-sample').dataTable({
                "aLengthMenu": [
                    [5, 15, 20, -1],
                    [5, 15, 20, "All"]
                ],
                "iDisplayLength": 5,
                "sDom": "<'row'<'col-lg-6'l><'col-lg-6'f>r>t<'row'<'col-lg-6'i><'col-lg-6'p>>",
                "sPaginationType": "bootstrap",
                "oLanguage": {
                    "sLengthMenu": "_MENU_ records per page",
                    "oPaginate": {
                        "sPrevious": "Prev",
                        "sNext": "Next"
                    }
                },
                "aoColumnDefs": [{
                    'bSortable': false,
                    'aTargets': [0]
                }]
            });
            jQuery('#editable-sample_wrapper .dataTables_filter input').addClass("form-control medium");
            jQuery('#editable-sample_wrapper .dataTables_length select').addClass("form-control xsmall");
            var nEditing = null;
            $('#editable-sample_new').click(function (e) {
                console.log("call 新增数据...");
                e.preventDefault();
                var aiNew = oTable.fnAddData(['', '', '', '', '', '', '<a class="save" href=""><i class="fa fa-save">保存&emsp;</i></a> <a class="cancel" href=""><i class="fa fa-undo">取消;</i></a>']);
                var nRow = oTable.fnGetNodes(aiNew[0]);
                editRow(oTable, nRow, true);
                nEditing = nRow;
            });

            $('#editable-sample a.save').live('click', function (e) {
                console.log("call a.save...");
                e.preventDefault();
                var all_datas = {};
                var dataset_name = $('#dataset_name')[0].innerText;
                var record_id = $(this).parents('tr').children()[0].innerText;
                all_datas["datas"] = {
                    "pcap_md5":  $(this).parents('tr').children()[1].innerText,
                    "payload_ascii":  $(this).parents('tr').children()[2].innerText,
                    "word_segmentation_text":  $(this).parents('tr').children()[3].innerText,
                    "word_tag_text":  $(this).parents('tr').children()[4].innerText,
                    "captured_date":  $(this).parents('tr').children()[5].innerText,
                }
                if ($(this).attr("data-mode") == "new") {
                    all_datas["url"] = "/aimales/dataset/" + dataset_name + "/edit/create/" + record_id;
                }else{
                    all_datas["url"] = "/aimales/dataset/" + dataset_name + "/edit/modify/" + record_id;
                }
                var a_node = $(this)[0];
                var tr_node = $(this).parent().parent();
                var nRow = $(this).parents('tr')[0];
                var td_nodes = tr_node[0].children;
                td_nodes[0].firstChild.innerText = record_id;
                td_nodes[0].firstChild.removeAttribute("readonly");
                console.log(td_nodes[0]);
                tr_node[0][0];
                $.ajax({
                    type: "POST",
                    url: all_datas["url"],
                    data: all_datas["datas"],
                    dataType: "json",
                    complete: function(data, status){
                        if(status != 'error'){
                            status = true;
                        }else{
                            alert("提交成功");
                            //var nRow = $(this).parents('tr')[0];
                            //oTable.fnDeleteRow(nRow);
                            status = false;
                            if(a_node.getAttribute("data-mode") == "new"){
                                $('tr:last').after(tr_node);
                            }
                        }
                    }
                });
            });

            // 删除记录
            $('#editable-sample a.delete').live('click', function (e) {
                console.log("call a.delete...");
                e.preventDefault();
                if (confirm("确定删除此条记录？") == false) {
                    return;
                }
                var dataset_name = $('#dataset_name')[0].innerText;
                var record_id = $(this).parents('tr').children()[0].innerText;
                var pcap_md5 = $(this).parents('tr').children('#pcap_md5')[0].innerText;
                var payload_ascii = $(this).parents('tr').children('#payload_ascii')[0].innerText;
                var word_segmentation_text = $(this).parents('tr').children('#word_segmentation_text')[0].innerText;
                var word_tag_text = $(this).parents('tr').children('#word_tag_text')[0].innerText;
                var captured_date = $(this).parents('tr').children('#captured_date')[0].innerText;
            
                $.ajax({
                    type: "POST",
                    url: "/aimales/dataset/" + dataset_name + "/edit/delete/" + record_id,
                    data: {
                        "pcap_md5": pcap_md5,
                        "payload_ascii": payload_ascii,
                        "word_segmentation_text": word_segmentation_text,
                        "word_tag_text": word_tag_text,
                        "captured_date": captured_date,
                    },
                    dataType: "json",
                    complete: function(data, status){
                       alert("提交成功");
                       if(status == 'error'){
                           status = true;
                       }else{
                            var nRow = $(this).parents('tr')[0];
                            oTable.fnDeleteRow(nRow);
                           status = false;
                       }
                    }
                });
            });

            // 取消新增数据记录
            $('#editable-sample a.cancel').live('click', function (e) {
                console.log("call a.cancel...");
                e.preventDefault();
                if ($(this).attr("data-mode") == "new") {
                    var nRow = $(this).parents('tr')[0];
                    oTable.fnDeleteRow(nRow);
                } else {
                    restoreRow(oTable, nEditing);
                    nEditing = null;
                }
            });
            
            // 保存编辑结果
            $('#editable-sample a.edit').live('click', function (e) {
                console.log("call a.edit...");
                e.preventDefault();
                var dataset_name = $('#dataset_name')[0].innerText;
                var record_id = $(this).parents('tr').children()[0].innerText;
                var pcap_md5 = $(this).parents('tr').children('#pcap_md5')[0].innerText;
                var payload_ascii = $(this).parents('tr').children('#payload_ascii')[0].innerText;
                var word_segmentation_text = $(this).parents('tr').children('#word_segmentation_text')[0].innerText;
                var word_tag_text = $(this).parents('tr').children('#word_tag_text')[0].innerText;
                var captured_date = $(this).parents('tr').children('#captured_date')[0].innerText;
            
                $.ajax({
                    type: "POST",
                    url: "/aimales/dataset/" + dataset_name + "/edit/delete/" + record_id,
                    data: {
                        "pcap_md5": pcap_md5,
                        "payload_ascii": payload_ascii,
                        "word_segmentation_text": word_segmentation_text,
                        "word_tag_text": word_tag_text,
                        "captured_date": captured_date,
                    },
                    dataType: "json",
                    complete: function(data, status){
                       if(status == 'error'){
                           status = true;
                           return false;
                       }else{
                            alert("提交成功");
                            status = false;
                       }
                    }
                });
                var nRow = $(this).parents('tr')[0];
                if (nEditing !== null && nEditing != nRow) {
                    //restoreRow(oTable, nEditing);
                    editRow(oTable, nRow);
                    nEditing = nRow;
                } else if (nEditing == nRow && $(this).children()[0].innerText == "保存") {
                    saveRow(oTable, nEditing);
                    nEditing = null;
                    alert("Updated! Do not forget to do some ajax to sync with backend :)");
                } else {
                    editRow(oTable, nRow);
                    nEditing = nRow;
                }
            });
        }
    };
}();