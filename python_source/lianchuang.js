
(function (window, $, uni) {
    //联创大型仪器管理系统前端公共方法库
    var pro = {
        //版本
        v: "1.0",
        //版权信息
        copyright: "杭州联创信息技术有限公司",
        //产品
        product: "",
        //语言 语言字典对象
        language: undefined,
        //语言翻译
        translate: function (key) {
            var dic = this.language;
            if (!dic) return key;
            if (typeof (key) == "string") {
                if (dic[key]) {
                    return dic[key];
                }
                else {
                    dic.forEach(function (value, index, array) {
                        GetSimilStr(key,array[index].name, array[index].value);
                        //code something

                    });
                   
                }
                return key;
            }
            else if (typeof (key) == "object") {
                $("span.uni_trans", key).each(function () {
                    $(this).html(uni.translate($(this).text()));
                });
                return key;
            }
            return "";
        },
        //初始化语言
        initLanguage: function (suc) {
            pro.j.util.initLangDic(suc);
        },
        //设置语言
        setLanguage: function (language) {
            pro.j.util.setLanguage(language);
        },
        //pro文件夹路径
        dir: (function () {
            var path;
            var i = location.href.toLowerCase().indexOf("/clientweb/");
            if (i < 0) path = location.origin;
            else path = location.href.substring(0, i);
            path += "/ClientWeb/pro/";
            return path;
        })(),
        //用户对象
        acc: {
            id: null,
            accno: null,
            name: null,
            phone: null,
            email: null,
            ident: null,
            dept: null,
            tutor: null,
            tutorid: null,
            tsta: null,
            rtsta: null,
            pro: null,
            score: null,
            credit:null,
            role: 0
        },
        //设备对象 兼容类型对象
        dev: {
            id: null,
            name: null,
            cps: null,
            dept: null,
            lab: null,
            url: null,
            pro: null,
            sta: null,
            early: null,
            last: null,
            max: null,
            min: null,
            maxuser: null,
            minuser: null,
            limit: null,
            memo: null
        },
        //学期信息
        term: {
            year: null,
            name: null,
            status: null,
            start: null,
            end: null,
            firstweek: null,
            totalweek: null,
            secnum: null,
            cts1: null,
            cts1start: null,
            cts1end: null,
            cts2: null,
            cts2start: null,
            cts2end: null
        },
        confirm: function (msg, okFun, bkFun, title, para) {
            uni.confirm(msg, okFun, bkFun, title, para);
        },
        //检查返回值
        ckV: function (rlt, suc, fail) {
            if (rlt == undefined) {
                uni.msgBox("返回了空值！", null, null, "error");
                return false;
            }
            else {
                if (rlt.ret == 0) {
                    if (fail == undefined) { uni.msgBox(rlt.msg, null, null, "warning"); uni.log.set("msg", rlt.msg + "/" + rlt.act); }
                    else fail(rlt);
                }
                else if (rlt.ret > 0) {
                    if (suc == undefined) { uni.msgBox(rlt.msg, null, null, "success"); uni.log.set("msg", rlt.msg + "/" + rlt.act); }
                    else suc(rlt);
                }
                else if (rlt.ret == -1) {//登录超时
                    uni.msgBox(rlt.msg, "", function () { location.reload(); }, "warning");
                    uni.log.set("msg", rlt.msg + "/" + rlt.act);
                }
                return true;
            }
        }

    }
    function GetSimilStr(szSer, szXml, szValue) {
        debugger;
        var szList = new Array();
        szList = szXml.split('$');

        var szValueList = new Array();
        szValueList = szValue.split('$');

        var bResSimel = true;
        for (var i = 0; i > szList.length; i++) {
            if (!(szSer.indexOf(szList[i]) > -1)) {
                bResSimel = false;
                return "";
            }
        }
        for (var i = 0; i < szValueList.length; i++) {
            try {
                szSer = szSer.replace(szList[i], szValueList[i]);
            }
            catch (error) {
            }
        }
        return szSer;
    }
    //ajax操作方法库（net）
    pro.j = {
        //post方式 form提交 拓展方法
        fPostS: function (url, act, $f, suc, fail, err) {
            var data = {};
            data.act = act;
            data.$f = $f;
            uni.j.fPost(url, data, function (rlt) {
                pro.ckV(rlt, suc, fail);
            }, err);
        },
        //post方式 js对象提交 拓展方法
        objPostS: function (url, obj, suc, fail) {
            uni.j.post(url, obj, function (rlt) {
                pro.ckV(rlt, suc, fail);
            });
        },
        //get方式 form提交 拓展方法
        fGetS: function (url, act, $f, suc, fail, err) {
            var data = {};
            data.act = act;
            data.$f = $f;
            uni.j.fGet(url, data, function (rlt) {
                pro.ckV(rlt, suc, fail);
            }, err);
        },
        //get方式 js对象提交 拓展方法
        objGetS: function (url, obj, suc, fail) {
            uni.j.objGet(url, obj, function (rlt) {
                pro.ckV(rlt, suc, fail);
            });
        }
    }
    //应用程序相关操作
    pro.j.app = {
        //路径
        p: pro.dir + "ajax/app.aspx",
        appAct:function(data,suc,fail){
            pro.j.objPostS(this.p,data,suc,fail);
        },
        //初始化应用程序
        initApp: function (para, fun) {
            para = para || {};
            para.act = "init_app";
            this.appAct(para, function (rlt) {
                if (rlt.data.acc) {
                    pro.acc = rlt.data.acc;
                }
                fun(rlt);
            });
        }
    }
    //登录相关操作
    pro.j.lg = {
        //路径
        p: pro.dir + "ajax/login.aspx",
        _login: function (data, suc, fail) {
            pro.j.objGetS(this.p, data, suc, fail);
        },
        //初始化用户对象
        initAcc: function (suc) {
            this._login({ "act": "init_acc" }, function (rlt) {
                if (rlt.data && rlt.data.id) {
                    pro.acc = rlt.data;
                }
                if (suc) suc(rlt);
            }, function () { })
        },
        //判断登录
        isLogin: function (suc, fail) {
            this._login({ "act": "is_login" }, suc, fail)
        },
        //登录
        login: function (id, pwd, suc, role) {
            var data = { "act": "login", "id": id, "pwd": pwd, "role": role };
            this._login(data, suc);
        },
        //验证码登录
        dLogin: function (id, pwd, num, suc, role) {
            var data = { "act": "dlogin", "id": id, "pwd": pwd, "number": num, "role": role };
            this._login(data, suc);
        },
        //激活并登录
        act: function (id, pwd, phone, email, suc, role) {
            var data = { "act": "act", "id": id, "pwd": pwd, "phone": phone, "email": email, "role": role };
            this._login(data, suc);
        },
        //帐号是否存在
        isExist: function (id, suc, fail) {
            var data = { "act": "is_exist", "id": id };
            pro.j.objGetS(this.p, data, suc, fail);
        },
        //退出登录
        logout: function (url) {
            uni.j.get(this.p + "?act=logout", function (rlt) {
                if (rlt.ret == 2) {//第三方登录退出
                    var path;
                    var i = location.href.toLowerCase().indexOf("/clientweb/");
                    if (i < 0) path = location.origin;
                    else path = location.href.substring(0, i);
                    location.href = path + "/LoginAll.aspx?op=logout"
                }
                else {
                    if (url)
                        location.href = url;
                    else
                        location.reload();
                }
            });
        },
        //form方式操作
        fLogin: function (act, $f, suc, fail) {
            pro.j.fPostS(this.p, act, $f, suc, fail);
        }
    }
    //账户相关操作
    pro.j.acc = {
        //路径
        p: pro.dir + "ajax/account.aspx",
        accAct: function (acc, suc, fail) {
            pro.j.objGetS(this.p, acc, suc, fail);
        },
        //通过登录名获取账户
        getAccById: function (id, suc) {
            var acc = {};
            acc.act = "get_acc_id";
            acc.id = id;
            this.accAct(acc, suc);
        },
        //通过姓名获取账户
        getAccByName: function (name, suc, ident) {
            var acc = {};
            acc.act = "get_acc_name";
            acc.name = name;
            acc.ident = ident;
            this.accAct(acc, suc);
        },
        //通过标识获取账户
        getAccByAccNo: function (accno, suc) {
            var acc = {};
            acc.act = "get_acc_accno";
            acc.accno = accno;
            this.accAct(acc, function (rlt) {
                var list = rlt.data;
                if (list.length > 0) {
                    rlt.data = list[0];
                    suc(rlt);
                }
                else {
                    uni.msg.warning("未获取到账户");
                }
            });
        },
        //申请实验室使用资格
        applyLabUseRole: function (lab_id, role_id, apply_id, up_file, suc) {
            var para = {};
            para.act = "apply_lab_use_role";
            para.lab_id = lab_id;
            para.role_id = role_id;
            para.apply_id = apply_id;
            para.up_file = up_file;
            this.accAct(para, suc);
        },
        //申请使用资格
        applyUseRole: function (role_id, apply_id, para, suc) {
            var obj = para ? uni.getObj(para) : {};
            obj.act = "apply_use_role";
            obj.role_id = role_id;
            obj.apply_id = apply_id;
            this.accAct(obj, suc);
        },
        //通过姓名获取导师
        getTutorByName: function (name, suc, fail) {
            var acc = {};
            acc.act = "get_tutor_name";
            acc.stu_name = name;
            this.accAct(acc, suc, fail);
        },
        //更新用户信息 主联系方式
        upContact: function (phone, email, suc, para) {
            var acc = para ? uni.getObj(para) : {};
            acc.act = "update_contact";
            acc.phone = phone;
            acc.email = email;
            this.accAct(acc, suc);
        },
        //更新用户信息含导师
        upInfoTu: function (phone, email, tutor_accno, tutor_name, suc) {
            var acc = {};
            acc.act = "update_tutor";
            acc.phone = phone;
            acc.email = email;
            acc.stu_accno = tutor_accno;
            acc.stu_name = tutor_name;
            this.accAct(acc, suc);
        },
        //解除微信绑定
        deleteWeChat: function (suc) {
            var acc = {};
            acc.act = "del_wechat";
            this.accAct(acc, suc);
        },
        //修改密码
        changePwd: function (old_pwd, pwd1, pwd2, suc) {
            pro.j.lg.login(pro.acc.id, old_pwd, function () {
                if (pwd1 != pwd2) {
                    uni.msgBox("两次密码不一致");
                    return;
                }
                var acc = {};
                acc.act = "update_pwd";
                acc.pwd = pwd1;
                pro.j.acc.accAct(acc, suc);
            });
        },
        //更新用户信息含导师(无需导师确认)
        upInfoTuCked: function (phone, email, tutor_accno, tutor_name, suc) {
            var acc = {};
            acc.act = "update_tutor_cked";
            acc.phone = phone;
            acc.email = email;
            acc.stu_accno = tutor_accno;
            acc.stu_name = tutor_name;
            this.accAct(acc, suc);
        },
        //成员指定导师
        assignTutor: function (tutor_accno, tutor_name, suc) {
            var acc = {};
            acc.act = "assign_tutor";
            acc.stu_accno = tutor_accno;
            acc.stu_name = tutor_name;
            this.accAct(acc, suc);
        },
        //成员指定导师(无需导师确认 自动创建项目:rtest=auto)
        assignTuCked: function (tutor_accno, tutor_name, suc, para) {
            var acc = para ? uni.getObj(para) : {};
            acc.act = "assign_tutor_cked";
            acc.stu_accno = tutor_accno;
            acc.stu_name = tutor_name;
            this.accAct(acc, suc);
        },
        tutorRel: function (order, accno, name, suc, id) {
            var t = {};
            t.act = "tutor_rel";
            t.order = order;
            if (id != undefined)
                t.stu_id = id;
            else
                t.stu_accno = accno;
            t.stu_name = name;
            this.accAct(t, suc);
        },
        //导师清除成员申请
        tutorDelRel: function (accno, suc) {
            this.tutorRel("del", accno, "", suc);
        },
        //导师确认成员
        tutorOkRel: function (accno, name, suc) {
            this.tutorRel("ok", accno, name, suc);
        },
        //导师否认成员
        tutorFailRel: function (accno, name, suc) {
            this.tutorRel("fail", accno, name, suc);
        },
        //导师清除成员申请
        tutorDelRelById: function (id, suc) {
            this.tutorRel("del", null, "", suc, id);
        },
        //导师确认成员
        tutorOkRelById: function (id, name, suc) {
            this.tutorRel("ok", null, name, suc, id);
        },
        //导师否认成员
        tutorFailRelById: function (id, name, suc) {
            this.tutorRel("fail", null, name, suc, id);
        },
        //form方式操作
        fAcc: function (act, $f, suc, fail) {
            pro.j.fPostS(this.p, act, $f, suc, fail);
        }
    }
    //组相关操作
    pro.j.group = {
        //路径
        p: pro.dir + "ajax/group.aspx",
        groupAct: function (g, suc, fail) {
            pro.j.objGetS(this.p, g, suc, fail);
        },
        //获取组信息
        getGroupById: function (group_id, suc) {
            var g = {};
            g.act = "get_g_info";
            g.group_id = group_id;
            this.groupAct(g, function (rlt) {
                if (rlt.data.length == 1) {
                    rlt.data = rlt.data[0];
                    suc(rlt);
                }
                else {
                    uni.msg.warning("未找到组");
                }
            });
        },
        //获取组成员
        getMbs: function (group_id, suc) {
            var g = {};
            g.act = "get_g_mbs";
            g.group_id = group_id;
            this.groupAct(g, suc);
        },
        //添加组成员
        addMem: function (group_id, id, suc) {
            pro.j.rtest.addMem(group_id, id, suc);
        },
        //添加多个组成员
        addMbs: function (group_id, mbs, suc) {
            var g = {};
            g.act = "add_g_mb";
            g.id = mbs;
            g.group_id = group_id;
            this.groupAct(g, suc);
        },
        //删除组成员
        delMem: function (group_id, id, suc) {
            var g = {};
            g.act = "del_g_mb";
            g.id = id;
            g.group_id = group_id;
            this.groupAct(g, suc);
        },
        //删除组成员byAccNo
        delMemByAccNo: function (group_id, accno, suc) {
            var g = {};
            g.act = "del_g_mb_accno";
            g.group_id = group_id;
            g.accno = accno;
            this.groupAct(g, suc);
        },
        //修改组名
        setGroupName: function (group_id, group_name, suc) {
            var g = {};
            g.act = "set_group_name";
            g.group_id = group_id;
            g.group_name = group_name;
            this.groupAct(g, suc);
        },
        //删除组
        delGroup: function (group_id, suc) {
            var g = {};
            g.act = "del_group";
            g.group_id = group_id;
            this.groupAct(g, suc);
        }
    }
    //科研项目相关操作
    pro.j.rtest = {
        //路径
        p: pro.dir + "ajax/rtest.aspx",
        rtestAct: function (test, suc, fail) {
            pro.j.objGetS(this.p, test, suc, fail);
        },
        //新建项目
        creRTest: function (name, level, ld_accno, ld_name, mbs, suc) {
            var test = {};
            test.act = "new";
            test.rt_name = name;
            test.rt_fee = rt_fee;
            test.rt_level = level;
            test.ld_accno = ld_accno;
            test.ld_name = ld_name;
            test.mb_list = mbs;
            this.rtestAct(test, suc);
        },
        //按照id获取项目
        getRTest: function (id, suc) {
            var test = {};
            test.act = "get_rt_info";
            test.rt_id = id;
            this.rtestAct(test, suc);
        },
        //获取全部项目
        getAllRTest: function (suc) {
            var test = {};
            test.act = "srch_rt";
            this.rtestAct(test, suc);
        },
        //搜索项目
        srchRTest: function (id, name, tutor_accno, leader_accno, suc) {
            var test = {};
            test.act = "srch_rt";
            test.rt_id = id;
            test.rt_name = name;
            test.tutor_accno = tutor_accno;
            test.leader_accno = leader_accno;
            this.rtestAct(test, suc);
        },
        //删除项目
        delRTest: function (id, suc) {
            var test = {};
            test.act = "del";
            test.id = id;
            this.rtestAct(test, suc);
        },
        //获取项目成员
        getRTMem: function (rt_id, suc) {
            var mb = {};
            mb.act = "get_rt_mb";
            mb.rt_id = rt_id;
            this.rtestAct(mb, suc);
        },
        //添加项目成员
        addRTMem: function (rt_id, group_id, id, suc) {
            var mb = {};
            mb.act = "add_rt_mb";
            mb.rt_id = rt_id;
            mb.group_id = group_id;
            mb.id = id;
            this.rtestAct(mb, suc);
        },
        //删除项目成员
        delRTMem: function (rt_id, group_id, id, suc) {
            var mb = {};
            mb.act = "del_rt_mb";
            mb.rt_id = rt_id;
            mb.group_id = group_id;
            mb.id = id;
            this.rtestAct(mb, suc);
        },
        //添加组成员
        addMem: function (group_id, id, suc) {
            var mb = {};
            mb.act = "add_g_mb";
            mb.group_id = group_id;
            mb.id = id;
            this.rtestAct(mb, suc);
        },
        //删除组成员
        delMem: function (group_id, id, suc) {
            var mb = {};
            mb.act = "del_g_mb";
            mb.group_id = group_id;
            mb.id = id;
            this.rtestAct(mb, suc);
        },
        //form方式操作
        fRTest: function (act, $f, suc) {
            pro.j.fGetS(this.p, act, $f, suc);
        }
    }
    pro.j.dev = {
        //路径
        p: pro.dir + "ajax/device.aspx",
        _devAct: function (obj, suc) {
            pro.j.objGetS(this.p, obj, suc);
        },
        //获取设备信息
        getDevById: function (id, suc) {
            var para = { act: "dev_filter", id: id };
            this._devAct(para, function (rlt) {
                var list = rlt.data.devs;
                if (list && list.length > 0) {
                    rlt.data = list[0];
                    suc(rlt);
                }
                else
                    uni.msgBox("找不到设备", null, null, "warning");
            });
        },
        //获取设备坐标列表
        getDevCoord: function (p, suc) {
            var para = p ? uni.getObj(p) : {};
            para.act = "get_dev_coord";
            this._devAct(para, suc);
        },
        setDevCoord: function (p, data, suc) {
            var para = p ? uni.getObj(p) : {};
            para.data = data;
            para.act = "set_dev_coord";
            pro.j.objPostS(this.p, para, suc);
        },
        //设备筛选
        devFilter: function (fl, suc) {
            fl.act = "dev_filter";
            this._devAct(fl, suc);
        },
        //获取预约状态
        getRsvSta: function (ds, suc) {
            ds.act = "get_rsv_sta";
            this._devAct(ds, suc);
        },
        //获取设备预约状态
        getDevRsvSta: function (id, date, suc, para) {
            var ds = para ? uni.getObj(para) : {};
            ds.dev_id = id;
            ds.date = date;
            this.getRsvSta(ds, function (rlt) {
                var list = rlt.data;
                if (list && list.length > 0) {
                    rlt.data = list[0];
                    suc(rlt);
                }
                else if (typeof (para.fail) == "function")
                    para.fail(rlt);
                else
                    uni.msgBox("获取设备预约状态失败", null, null, "warning");
            });
        },
        //获取设备类型预约状态
        getDevKindRsvSta: function (id, date, suc, para) {
            var ds = para ? uni.getObj(para) : {};
            date = date.replace(/-/g, '');
            ds.kind_id = id;
            ds.date = date;
            ds.iskind = 'true';
            this.getRsvSta(ds, function (rlt) {
                var list = rlt.data;
                if (list && list.length > 0) {
                    rlt.data = list[0];
                    suc(rlt);
                }
                else if (typeof (para.fail) == "function")
                    para.fail(rlt);
                else
                    uni.msgBox("获取设备类型预约状态失败", null, null, "warning");
            });
        },
        ////获取设备空闲状态
        //ckFree: function (id, date, start, end,suc) {
        //    var para = {};
        //    para.dev_id = id;
        //    para.date = date;
        //    para.start = start;
        //    para.end = end;
        //    para.act = "ck_free";
        //    this._devAct(para, suc);
        //},
        //form方式操作
        fDev: function (act, $f, suc) {
            pro.j.fGetS(this.p, act, $f, suc);
        }
    }
    //房间相关
    pro.j.rm = {
        //路径
        p: pro.dir + "ajax/room.aspx",
        rmAct: function (obj, suc) {
            pro.j.objGetS(this.p, obj, suc);
        },
        //获取房间预约状态
        getRsvSta: function (date, suc, para) {
            var ds = para ? uni.getObj(para) : {};
            ds.date = date;
            ds.act = "get_rsv_sta";
            this.rmAct(ds, suc);
        },
        //获取房间组合预约状态
        getRGRsvSta: function (date, suc, para) {
            var ds = para ? uni.getObj(para) : {};
            ds.date = date;
            ds.act = "get_rm_group_sta";
            this.rmAct(ds, suc);
        },
        //获取房间组合
        getRmGroup: function (room_id, num, suc) {
            var ds = {};
            ds.room_id = room_id;
            ds.num = num;
            ds.act = "get_rm_group";
            this.rmAct(ds, suc);
        }
    }
    //教学实验相关
    pro.j.test = {
        //路径
        p: pro.dir + "ajax/teachtest.aspx",
        testAct: function (obj, suc) {
            pro.j.objPostS(this.p, obj, suc);
        },
        //修改试验计划状态
        setPlanStatus: function (plan_id, status, suc, para) {
            var obj = para || {};
            obj.plan_id = plan_id;
            obj.status = status;
            obj.act = "set_plan_status";
            this.testAct(obj, suc);
        },
        //获取实验项目列表
        getTestitemList: function (plan_id, course_id, suc) {
            var obj = {};
            obj.plan_id = plan_id;
            obj.course_id = course_id;
            obj.act = "get_testitem";
            this.testAct(obj, suc);
        },
        //实验报告评分
        correctReport: function (sid, accno, score, eval, suc) {
            var cor = {};
            cor.act = "report_correct";
            cor.sid = sid;
            cor.accno = accno;
            cor.score = score;
            cor.eval = eval;
            this.testAct(cor, suc);
        },
        //删除实验计划
        delTestPlan: function (plan_id, suc) {
            var plan = {};
            plan.act = "del_plan";
            plan.plan_id = plan_id;
            this.testAct(plan, suc);
        },
        //删除实验项目
        delTestitem: function (test_id,card_id, suc) {
            var test = {};
            test.act = "del_testitem";
            test.test_id = test_id;
            test.card_id = card_id;
            this.testAct(test, suc);
        },
        //上传实验报告
        uploadReport: function (sid, file, suc) {
            var para = {};
            para.act = "report_upload";
            para.sid = sid;
            para.file = file;
            this.testAct(para, suc);
        }
    }
    //预约相关操作
    pro.j.rsv = {
        //路径
        p: pro.dir + "ajax/reserve.aspx",
        rsvAct: function (para, suc, fail) {
            pro.j.objGetS(this.p, para, suc, fail);
        },
        //获取获取预约操作信息
        getSignResv: function (id, suc) {
            var rsv = {};
            rsv.act = "sign_resv";
            rsv.ResvID = id;
            this.rsvAct(rsv, suc);
        },
        //快速预约
        quickResv: function (para,suc) {
            var rsv = para || {};
            rsv.act = "quick_resv";
            this.rsvAct(rsv, suc);
        },
        //删除科研实验
        delRTRsv: function (id, suc) {
            var rsv = {};
            rsv.act = "del_rt_resv";
            rsv.id = id;
            this.rsvAct(rsv, suc);
        },
        //审核科研实验
        ckRTRsv: function (id, order, suc) {
            var obj = {};
            obj.act = "ck_rtrsv";
            obj.id = id;
            obj.order = order;
            this.rsvAct(obj, suc);
        },
        //审核通过
        ckRTRsvOk: function (id, suc) {
            this.tutorCkRTRsv(id, "ok", suc);
        },
        //审核不通过
        ckRTRsvFail: function (id, suc) {
            this.tutorCkRTRsv(id, "fail", suc);
        },
        //获取设备科研预约列表
        getRTRsvList: function (dev_id, start, end, suc) {
            var rsv = {};
            rsv.act = "get_dev_rtrsv_list";
            rsv.dev_id = dev_id;
            rsv.start = start;
            rsv.end = end;
            this.rsvAct(rsv, suc);
        },
        //获取设备预约列表
        getResvList: function (dev_id, start, end, suc) {
            var rsv = {};
            rsv.act = "get_resv_list";
            rsv.dev_id = dev_id;
            rsv.start = start;
            rsv.end = end;
            this.rsvAct(rsv, suc);
        },
        //获取个人预约
        getMyResv: function (suc, para) {
            var rsv = para || {};
            rsv.act = "get_my_resv";
            this.rsvAct(rsv, suc);
        },
        //获取服务器当前时间
        getServertime: function (suc, para) {
            var rsv = para || {};
            rsv.act = "get_my_servertime";
            this.rsvAct(rsv, suc);
        },
        //获取设备科研预约表单数据
        getRTRsvFm: function (dev_id, date, suc) {
            var fm = {};
            fm.act = "get_dev_rtrsv_fm";
            fm.dev_id = dev_id;
            fm.date = date;
            this.rsvAct(fm, suc);
        },
        //获取设备科研预约费用数据
        getRTRsvFee: function (dev_id, rt_id, suc) {
            var get = {};
            get.act = "get_dev_rtrsv_fee";
            get.dev_id = dev_id;
            get.rt_id = rt_id;
            this.rsvAct(get, suc);
        },
        //提交设备科研预约表单
        subRTRsvFm: function ($f, suc) {
            this.fRsv("sub_dev_rtrsv_fm", $f, suc);
        },
        //获取场馆预约列表
        getYardRsvList: function (dev_id, start, end, suc) {
            var para = {};
            para.act = "get_dev_yard_rsv";
            para.dev_id = dev_id;
            para.start = start;
            para.end = end;
            this.rsvAct(para, suc);
        },
        //获取场馆预约
        getYardRsv: function (para, suc) {
            if (para)
                para.act = "get_dev_yard_rsv";
            this.rsvAct(para, suc);
        },
        //获取场馆预约审核行状态
        getYardRsvCheck: function (resv_id, suc) {
            var para = {};
            para.act = "get_yardrsv_checkinfo";
            para.resv_id = resv_id;
            this.rsvAct(para, suc);
        },
        //获取预约审核类型
        getCheckType: function (kind, main, suc) {
            var para = {};
            para.act = "get_check_type";
            para.ck_kind = kind;
            para.ck_main = main;
            this.rsvAct(para, suc);
        },
        //预约使用反馈
        setFeedback: function (resv_id, dev_id, con, kind, score, suc) {
            var para = {};
            para.act = "set_rsv_feedback";
            para.resv_id = resv_id;
            para.dev_id = dev_id;
            para.con = con;
            para.kind = kind;
            para.score = score;
            this.rsvAct(para, suc);
        },
        //获取预约使用反馈
        getFeedback: function (resv_id, dev_id, accno, suc) {
            var para = {};
            para.act = "get_rsv_feedback";
            para.resv_id = resv_id;
            para.dev_id = dev_id;
            para.accno = accno;
            this.rsvAct(para, suc);
        },
        //设置教学预约 resv_list格式 组编号&房间号组(,隔开)周次星期起始节次节次差 用;隔开
        setTchResv: function (term, test_id, resv_list, suc, para) {
            var rsv = para ? uni.getObj(para) : {};
            rsv.act = "set_tch_rsv";
            rsv.term = term;
            rsv.test_id = test_id;
            rsv.resv_list = resv_list;
            this.rsvAct(rsv, suc);
        },
        //删除预约
        delResv: function (id, suc, para,fail) {
            var rsv = para ? uni.getObj(para) : {};
            rsv.act = "del_resv";
            rsv.id = id;
            this.rsvAct(rsv, suc,fail);
        },
        //删除预约组
        delResvGroup: function (id, suc) {
            this.delResv(id, suc, { resv_type: "group" });
        },
        //确定预约生效
        decideResv: function (id, suc) {
            var rsv = {};
            rsv.act = "decide_resv";
            rsv.id = id;
            this.rsvAct(rsv, suc);
        },
        //删除活动安排
        delOpenAty: function (aty_id, resv_id, suc) {
            var rsv = {};
            rsv.act = "del_open_aty";
            rsv.aty_id = aty_id;
            rsv.resv_id = resv_id;
            this.rsvAct(rsv,suc);
        },
        //提前结束预约
        finish: function (id, suc, msg) {
            pro.confirm(msg || uni.translate("确定要提前结束预约？"), function () {
                var p = {};
                p.act = "resv_leave";
                p.type = 2;
                p.resv_id = id;
                pro.j.rsv.rsvAct(p, suc || function () {
                    uni.msgBoxR(uni.translate("操作成功！"), null, null, "success");
                }, function () {
                    uni.msgBox(uni.translate("操作失败，请确保已开始使用。"));
                });
            });
            //uni.confirm(msg || "是否提前结束?", function () {
            //    var rsv = {};
            //    rsv.act = "set_resv";
            //    rsv.resv_id = id;
            //    rsv.cut = "true";
            //    pro.j.rsv.rsvAct(rsv, suc || function () {
            //        uni.msgBoxR("操作成功！", null, null, "success");
            //    });
            //});
        },
        //获取课程预约
        getTchResv: function (start, end, suc, para) {
            var rsv = para ? uni.getObj(para) : {};
            rsv.act = "get_tch_resv";
            rsv.start = start;
            rsv.end = end;
            this.rsvAct(rsv, suc);
        },
        //获取实验计划预约
        getTestPlanResv: function (plan_id, term, suc) {
            var rsv = {};
            rsv.act = "get_plan_resv";
            rsv.plan_id = plan_id;
            rsv.term = term;
            this.rsvAct(rsv, suc);
        },
        //获取实验预约
        getTestResv: function (test_id, suc) {
            var rsv = {};
            rsv.act = "get_test_resv";
            rsv.test_id = test_id;
            this.rsvAct(rsv, suc);
        },
        //获取实验预约记录
        getTestResvInfo: function (term, suc, test_id, plan_id) {
            var rsv = {};
            rsv.act = "get_test_info";
            rsv.test_id = test_id;
            rsv.plan_id = plan_id;
            rsv.term = term;
            this.rsvAct(rsv, suc);
        },
        //获取第三方预约  未使用
        getThirdResvById: function (id, suc) {
            var rsv = {};
            rsv.act = "get_third_resv";
            rsv.resv_id = id;
            this.rsvAct(rsv, function (rlt) {
                if (rlt.data && rlt.data.length == 1) {
                    rlt.data = rlt.data[0];
                    suc(rlt);
                }
                else {
                    uni.msgBox("data not found");
                }
            });
        },
        //获取活动座位
        getAtySeats: function (aty_id, suc) {
            var rsv = {};
            rsv.act = "get_aty_seats";
            rsv.aty_id = aty_id;
            this.rsvAct(rsv, suc);
        },
        //加入活动
        enrollAty: function (para, suc) {
            var para = para || {};
            para.act = "enroll_aty";
            this.rsvAct(para, suc);
        },
        //退出活动
        quitAty: function (aty_id, suc) {
            var para = { act: "quit_aty", aty_id: aty_id };
            this.rsvAct(para, suc);
        },
        //form方式操作
        fRsv: function (act, $f, suc, fail, err) {
            pro.j.fGetS(this.p, act, $f, suc, fail, err);
        },
        ////获取验证图片
        SetNumberCode: function (para,suc) {
            var para = { act: "SetNumberCode"};
            this.rsvAct(para, suc);
        },
    }
    //实验数据
    pro.j.data = {
        //删除实验数据
        delTestData: function (id, suc) {
            var obj = {};
            obj.act = "del_data";
            obj.id = id;
            pro.j.util.utilAct(obj, suc);
        }
    }
    //文章
    pro.j.art = {
        //路径
        p: pro.dir + "ajax/article.aspx",
        //js对象参数
        artAct: function (obj, suc) {
            pro.j.objPostS(this.p, obj, suc);
        },
        //保存xml文章
        saveXmlArticle: function (con, id, type, suc, title, attrs, state, file) {
            var obj = {};
            obj.act = "save_xml_art";
            obj.content = "\"" + con + "\"";//注释掉特殊格式，便于数据传输
            obj.id = id;
            obj.type = type;
            obj.title = title;
            obj.attrs = attrs;
            obj.state = state;
            obj.file = file;
            this.artAct(obj, suc);
        },
        //form方式操作
        fArt: function (act, $f, suc) {
            pro.j.fGetS(this.p, act, $f, suc);
        }
    }
    //xml操作
    pro.j.xml = {
        //存储数据到xml
        save: function (data, id, type, suc, title, attrs, state, file) {
            pro.j.art.saveXmlArticle(data, id, type, suc, title, attrs, state, file);
        }
    }
    //科研成果操作
    pro.j.achi = {
        //路径
        p: pro.dir + "ajax/achieve.aspx",
        //js对象参数
        achiAct: function (obj, suc) {
            pro.j.objGetS(this.p, obj, suc);
        },
        //设置成果
        setAchi: function (obj, suc) {
            if (!obj) obj = {};
            obj.act = "set_achi";
            this.achiAct(obj, suc);
        },
        //删除成果
        delAchi: function (id, suc) {
            var obj = {};
            obj.achi_id = id;
            obj.act = "del_achi";
            this.achiAct(obj, suc);
        }
    }
    //其它操作
    pro.j.util = {
        //路径
        p: pro.dir + "ajax/util.aspx",
        //js对象参数
        utilAct: function (obj, suc) {
            pro.j.objGetS(this.p, obj, suc);
        },
        //初始化语言字典到uni.language
        initLangDic: function (suc) {
            var obj = {};
            obj.act = "get_language";
            pro.j.util.utilAct(obj, function (rlt) {
                if (rlt.data) {
                    uni.language = rlt.data;
                    if (suc) suc(rlt);
                }
            });
        },
        //设置语言
        setLanguage: function (language) {
            var obj = {};
            obj.act = "set_language";
            obj.language = language;
            pro.j.util.utilAct(obj, function () {
                location.reload();
            });
        },
        //获取费率
        getFee: function (para, suc) {
            var obj = para ? uni.getObj(para) : {};
            obj.act = "get_fee";
            this.utilAct(obj, suc);
        },
        //获取code表
        getCodeTbl: function (type, sn, suc) {
            var obj = { act: "get_code", type: type||'', sn: sn||'' };
            this.utilAct(obj, suc);
        },
        //投票
        setVote: function (vote_id, items,suc) {
            var obj = { act: "set_vote", vote_id: vote_id, item_v: items };
            this.utilAct(obj, suc);
        },
        //form方式操作
        fUtil: function (act, $f, suc) {
            pro.j.fGetS(this.p, act, $f, suc);
        }
    }

    var proj = pro.j;

    //获取费用
    pro.getFee2 = _UniGetFee2;
    function _UniGetFee2(unitFee, unitTime, totalTime, k) {
        if (!uni.isNoNull([unitFee, unitTime, totalTime])) {
            return 0;
        }
        uni.isNoNull(unitFee);
        if (totalTime <= 0 || unitTime <= 0) {
            return 0;
        }
        if (k != undefined && !isNaN(k)) {
            unitFee = parseFloat(unitFee);
            unitTime = parseFloat(unitTime);
            return parseFloat((_UniGetFee2(unitFee, unitTime, k) * (totalTime / k)).toFixed(2));
        }
        else {
            var vUintfee = parseFloat(unitFee);
            var vUintTime = parseFloat(unitTime);
            var vTotalTime = parseFloat(totalTime);
            return parseFloat((vUintfee * vTotalTime / vUintTime).toFixed(2));
        }
    }
    //判断登录
    pro.isLogin = function () {
        var acc = pro.acc;
        if (uni.isNull(acc.id)) {
            return false;
        } else {
            return true;
        }
    }
    //判断登录并弹出登录框
    pro.isloginL = function (para) {
        if (!pro.isLogin()) {
            if (typeof (cus) != 'undefined')
                cus.showLogin(para);//需要额外定义
            return false;
        }
        else {
            return true;
        }
    };
    //判断是否导师
    pro.isTutor = function (i) {
        return (parseInt(i) & 1048576) > 0;
    }
    //判断是否登录和导师审核状态
    pro.isloginTu = function () {
        if (pro.isloginL()) {
            var acc = pro.acc;
            var s = acc.tsta;
            if (s == "0" || s == "4") {
                return true;
            }
            else if (s == "1") {
                uni.msgBox("你还未指定导师，不能预约。<br/>请到[<a href='UserCenter.aspx?tab=4'>个人信息</a>]页面指定导师。");
                return false;
            }
            else if (s == "5" || s == undefined) {
                uni.msgBox("获取导师审核状态失败，请尝试重新登录。");
                return false;
            }
            else {
                uni.msgBox("你还未获取导师项目实验的许可。你可以到[<a href='UserCenter.aspx?tab=4'>个人信息</a>]页面查看导师审核状态。");
                return false;
            }
        }
        else {
            return false;
        }
    };
    //判断是否登录和项目状态
    pro.isloginRT = function () {
        if (pro.isloginL()) {
            var acc = pro.acc;
            var s = acc.rtsta;
            if (s == "1") {
                return true;
            }
            else {
                uni.msgBox("你还没有成功参与任何项目，请到[<a href='UserCenter.aspx?tab=2'>我的项目</a>]查看。");
                return false;
            }
        }
        return false;
    };

    //日期格式化
    pro.dt = {};
    //分钟转中文时间
    pro.dt.m2dms = function (m) {
        var t = parseInt(m);
        var dy = parseInt(t / 1440);
        var hr = parseInt((t % 1440) / 60);
        var mi = parseInt((t % 1440) % 60);
        return (dy ? dy + uni.translate('天') : "") + (hr ? hr + (dy ? uni.translate('时') : uni.translate('小时')) : "") + (mi ? mi + (hr ? uni.translate('分') : uni.translate('分钟')) : "");
    }
    pro.dt.m2ms = function (m) {
        var t = parseInt(m);
        var ms = parseInt(t / 60) + uni.translate('时');
        ms += parseInt(t % 60) + uni.translate('分');
        return ms;
    }
    //日期数字转日期字符串
    pro.dt.num2date = function (num) {
        num = "" + num;
        var str = "";
        if (num.length == 8) {
            str = num.substring(0, 4) + "-" + num.substring(4, 6) + "-" + num.substring(6);
        }
        return str;
    }
    //日期字符串转日期数字
    pro.dt.date2num = function (dt) {
        if (typeof (dt) == "string")
            return parseInt(dt.replace(/-/g, ""));
        else
            return 0;
    }
    //时间位补足两位
    pro.dt.timeFull = function (hm) {
        var tmp = hm.split(":");
        var h = uni.num2Str(tmp[0]);
        var m = uni.num2Str(tmp[1]);
        return h + ":" + m;
    }
    //日期或字符串转教学时间 term对象需初始化 教学时间(WWD)第几周WW，星期几D
    pro.dt.date2wwd = function (dt) {
        if (uni.isNull(pro.term.year)) return 0;
        var start = uni.parseDate(pro.term.start);
        var end = uni.parseDate(pro.term.end);
        var first = ((7 - start.getDay()) % 7) + 1;
        var date = typeof (dt) == 'object' ? dt : uni.parseDate(dt);
        if (uni.compareDate(date, end) > 0) return -1;
        var dt1 = start.getTime();
        var dt2 = date.getTime();
        var diff = parseInt((dt2 - dt1) / 1000 / 60 / 60 / 24);
        if (diff < 0) return -1;
        var ww = (diff < first) ? 1 : parseInt((diff - first) / 7) + 2;
        return ww * 10 + (6 - ((7 - date.getDay()) % 7));
    }
    pro.dt.wwd2date = function (wwd) {
        if (uni.isNull(pro.term.year)) return undefined;
        var start = uni.parseDate(pro.term.start);
        var first = ((7 - start.getDay()) % 7) + 1;
        var ww=parseInt(wwd / 10, 10);
        var d=(ww-2)*7+first+(wwd % 10)+1;
        return start.addDays(d-1);
    }
    //calendar公共对象
    pro.calendar = { instants: {} };
    //弹出窗口dlg扩展
    pro.d = {
        //窗口内关闭操作
        close: function (p) {
            $(p).parents(".dialog:first").dialog("close");
        },
        //参数转换
        getPara: function (para) {
            var p = "";
            if (typeof (para) != "undefine") {
                var pa = uni.obj2Url(para);
                if (pa.length > 0)
                    p = "?" + pa;
            }
            return p;
        }
    };
    //教学实验相关弹窗
    pro.d.test = {
        //创建实验计划
        crePlan: function (title, para, clsFun) {
            var p = pro.d.getPara(para);
            uni.dlgPage(pro.dir + "page/testplan/create.aspx" + p, title || "新建实验计划", 700, 560, clsFun);
        },
        //创建实验项目
        creTest: function (title, para, clsFun) {
            var p = pro.d.getPara(para);
            uni.dlgPage(pro.dir + "page/testitem/create.aspx" + p, title || "新建实验项目", 460, 380, clsFun);
        },
        //修改实验项目
        setTest: function (title, para, heigh, clsFun) {
            var p = pro.d.getPara(para);
            uni.dlgPage(pro.dir + "page/testitem/set.aspx" + p, title || "修改实验项目", 460, heigh || 420, clsFun);
        },
        //上传实验报告模版
        uploadFile: function (title, para, heigh, clsFun) {
            var p = pro.d.getPara(para);
            uni.dlgPage(pro.dir + "page/testitem/upload.aspx" + p, title || "上传实验报告模版", 460, heigh || 300, clsFun);
        }
    };
    //组管理
    pro.d.group = {
        //组管理
        manage: function (title, para, clsFun) {
            var p = pro.d.getPara(para);
            uni.dlgPage(pro.dir + "page/group/manage.aspx" + p, title || "成员管理", para.width || 480, para.heigh || 600, clsFun);
        }
    };
    //其它
    pro.d.other = {
        //预约须知
        resvNotice: function (title, para, clsFun) {
            var p = pro.d.getPara(para);
            uni.dlgPage(pro.dir + "page/other/notice.aspx" + p, title || "预约须知", para.width || 600, para.heigh || 600, clsFun);
        }
    }
    pro.d.basic = {
        noInit: function () { uni.msgBox("未加载dlg_basic", null, null, "error"); },
        //获取预约时间选择器
        addDateTimePicker: function (panel, obj, type) { this.noInit(); },
        //获取组管理器
        mGroupMembers: function (panel, opt) { this.noInit(); },
        //获取周期时间选择器
        cycleDateTimePicker: function ($panel, para) { this.noInit(); },
        //for周期时间选择器 计算周期时间
        analysisDateTime: function ($panel) { this.noInit(); }
    };
    pro.d.acc = {};
    pro.d.lg = {};
    pro.d.resv = {
        noInit: function () { uni.msgBox("未加载dlg_resv", null, null, "error"); },
        //修改时间
        alterTime: function (devId, devKind, resvId, start, end) { this.noInit(); }
    };
    pro.d.rtest = {};
    pro.d.role = {};

    //html格式化
    pro.htm = {
        getResvRule: function (obj) {
            var remark = $('<div><span>' + uni.translate('当日开放') + '：<span class="open_t"></span>；<span class="rule_limit"></span>；' + uni.translate('允许时长') + '：<span class="red rule_t_min"></span> - <span class="red rule_t_max"></span>；' + uni.translate('迟到') + ' <span class="red rule_t_cancel"></span> ' + uni.translate('取消预约') + '。</br>' + uni.translate('人数限制') + '：<span class="rule_user"></span>；<span class="rule_desc"></span></span></div>');
            var open = "";
            if (obj.ops && obj.ops.length > 0) {
                for (var i = 0; i < obj.ops.length; i++) {
                    var op = obj.ops[i];
                    open += '<span class="red open_t_start">' + op.start + '</span> - <span class="red open_t_end">' + op.end + '</span>，';
                }
                if (open.length > 0) open = open.substr(0, open.length - 1);
            }
            else
                open = '<span class="red open_t_start">' + obj.openStart + '</span> - <span class="red open_t_end">' + obj.openEnd + '</span>';
            $(".open_t", remark).html(open);
            $(".rule_user", remark).html((obj.maxUser == obj.minUser ? '' : '<span class="red rule_u_min">' + obj.minUser + '</span> - ') + '<span class="red rule_u_max">' + obj.maxUser + '</span>');
            if (obj.rule&&obj.rule!="&nbsp;") {
                var rl = uni.translate($("<div>" + obj.rule + "</div>"));
                $(".rule_desc", remark).html(uni.translate('预约属性') + '：<span class="grey">' + rl.html() + '</span>。');
            }
            var max = obj.max ? pro.dt.m2dms(obj.max) : "0";
            var min = obj.min ? pro.dt.m2dms(obj.min) : "0";
            var cancel = obj.cancel ? pro.dt.m2dms(obj.cancel) : "" + uni.translate("未限制") + "";
            $(".rule_t_max", remark).html(max);
            $(".rule_t_min", remark).html(min);
            $(".rule_t_cancel", remark).html(cancel);
            var limit;
            if (obj.islong && obj.earliest) {
                var earliest = new Date();
                var latest = new Date();
                earliest.addDays(parseInt(obj.earliest || 0) / 1440 - 1);
                latest.addDays(parseInt(obj.latest || 0) / 1440);
                limit = '' + uni.translate('允许日期') + '：<span class="red rule_t_latest">' + latest.format("yyyy/MM/dd") + '</span> - <span class="red rule_t_earliest">' + earliest.format("yyyy/MM/dd") + '</span>';
            }
            else {
                var earliest = obj.earliest ? pro.dt.m2dms(obj.earliest) : "0";
                var latest = obj.latest ? pro.dt.m2dms(obj.latest) : "0";
                limit = '' + uni.translate('预约至少提前') + '：<span class="red rule_t_latest">' + latest + '</span> ' + uni.translate('最长提前') + '：<span class="red rule_t_earliest">' + earliest + '</span>';
            }
            $(".rule_limit", remark).html(limit);
            return remark.html();
        }
    };
    //列表滚动
    pro.autoScroll = {
        //滚动
        scroll: function (obj, count, speed) {
            obj = $(obj);
            it = obj.children("tbody tr:first,li:first");
            it.animate({
                marginTop: -(it.height())
            }, speed, function () {
                $(this).css({ marginTop: "0" }).appendTo(obj);
            });
        },
        interval: function (selector, count, speed, ishr) {
            $(selector).each(function () {
                var pthis = $(this);
                var len = pthis.children("tbody tr,li").length;
                pthis.css({ overflow: "hidden"});
                if (len > count) {
                    pthis.css({ height: pthis.children("tbody tr:first,li:first").height() * count });
                }
            });
            return window.setInterval('$("' + selector + '").each(function () {if($(this).children("tbody tr,li").length >' + count + ') pro.autoScroll.scroll(this,' + count + ',' + (speed ? speed / 2 : 1000) + ');})', speed || 2000);
        },
        //注册滚动
        regist: function (selector, count, speed) {
            if (uni.hr.isHrLoad($(selector))) {//对象是hr加载需特殊处理
                uni.hr.loadSuccess(function () {
                    var sint = pro.autoScroll.interval(selector, count, speed);
                    uni.hr.loadRef(function () {
                        window.clearInterval(sint);
                    });
                });
            }
            else
                $(function () { pro.autoScroll.interval(selector, count, speed); });
        }
    };

    //-------------------------------jquery ui 拓展-----------------
    $.fn.extend({
        //autocomplete拓展
        procomplete: function (sel, rsp) {
            var _dir = pro.dir + "ajax/data/";
            var pthis = $(this);
            if (!uni.isNull(pthis.attr("url"))) {
                var para = pthis.attr("para");
                var url = _dir + pthis.attr("url") + "?type=" + (pthis.attr("act") || "") + "&" + (para || "");
                if (!rsp) rsp = function (event, ui) {
                    if (ui.content.length == 0) {
                        ui.content.push({ label: uni.translate("未找到任何数据") });
                    }
                }
                pthis.autocomplete({
                    minLength: 0,
                    source: url,
                    select: function (ev, ui) {
                        if (ui.item && ui.item.id && typeof (sel) == 'function')
                            sel(ui.item, ui);
                    },
                    response: function () {
                        return rsp;
                    }
                });
                pthis.click(function () {
                    var t = $(this)
                    if (t.val()) {
                        t.autocomplete("search", "");
                    }
                });
            }
            else {
                uni.msgBox("参数错误", null, null, "error");
                uni.log.set("msg", "参数错误!/pro_procomplete");
            }
        }
    });
    window.pro = pro;
})(window, jQuery, uni);

//---------------------------依赖bootstrap 插件拓展----------------
$.fn.extend({
    bsDropdown: function (para) {
        if (!uni.isBootstrap()) return;//判断是否加载bootstrap
        if (!para) para = {};
        $(this).each(function () {
            var sel = $(this);
            if (!sel.is("select")) return;
            var dft = "<span class='drop-select'>" + $("option:selected", sel).html() + "</span>&nbsp;";
            var ui = "default";
            var btns = "";
            if (para.ui) ui = para.ui;
            if (para.style == "btns") {
                btns = '<button type="button" class="dp_title btn" style="color: #333;background-color:#fff;border-color:#ccc;cursor:default;">' + dft + '</button>';
                dft = "";
            }
            var dd = $('<div class="btn-group">' + btns + '<button class="dp_list btn btn-' + ui + ' dropdown-toggle" type="button" data-toggle="dropdown">' + dft + '<span class="caret"></span></button>' +
  '<ul class="dropdown-menu" role="menu"></ul></div>');
            var dm = $(".dropdown-menu", dd);
            $("option", sel).each(function () {
                var op = $(this);
                var v = op.attr("value");
                var c = op.html();
                dm.append('<li role="presentation"><a role="menuitem" tabindex="-1" value=' + v + '>' + c + '</a></li>');
            });
            $("a", dm).click(function () {
                var p = $(this);
                var v = p.attr("value");
                var c = p.html();
                if (sel.val() != v) {
                    sel.val(v);
                    sel.trigger("change")
                }
                $(".drop-select", dd).html(c);
            });
            if (para.width)//最小宽度
                dd.find("button:first").css("min-width", para.width - 26);
            dd.find(".dp_title").unbind("focus").click(function () {
                if (dd.hasClass("open"))
                    dd.removeClass("open");
                else
                    dd.addClass("open");
            });
            sel.after(dd);
            sel.hide();
        });
    }
});

//---------------------------jqeury 插件拓展----------------
$.fn.extend({
    //异步上传 fileinput控件 file=(id与name) limit=后缀(无点，逗号分隔) dir=目录 save=指定存储名(小心替换)  (兄弟元素)存储名存于.up_file 默认[name=up_file] 文件名显示于.cur_file_name
    uploadFile: function (para, suc, fail) {
        var objs = $(this);
        if (!para) para = {};
        objs.each(function (i) {
            var obj = $(this);
            obj.attr("save_name", "");
            obj.attr("cur_name", "");
            var fl = obj.attr("file");//未指定fileinput控件
            if (!fl) {
                var choice = "choice_file_" + i + (new Date()).getTime();
                var sel_p = obj.parents(".up_file_panel:first").find(".choice_file_panel");//寻找选择文件区域
                var div = '<div class="file_name_input"><input type="file" name="' + choice + '" id="' + choice + '" class="click"></div>';
                if (sel_p.length == 1)
                    sel_p.html(div);
                else
                    obj.before(div);
                obj.attr("file", choice);
                fl = choice;
            }
            //替换丑按钮
            //var fler = $("#" + fl);
            //if (!uni.isIE()&&!fler.hasClass("rep")) {
            //    fler.addClass("rep").hide();
            //    fler.wrap("<div style='overflow: hidden;'></div>");
            //    var txt = uni.translate("未选择上传的文件");
            //    var tr_fler = $("<div class='file_replace_panel' style='line-height: 30px;cursor: pointer;'>" +
            //        "<span class='file_replace_btn' style='padding:6px;border:1px solid #ccc;'>"+uni.translate("选择文件")+"</span>&nbsp;<span class='dir'>"+txt+"</span></div>")
            //    .click(function () { fler.trigger("click"); });
            //    fler.change(function () {
            //        if (this.value == "") tr_fler.find(".dir").html(txt);
            //        else {
            //            var dirs = this.value.split("\\");
            //            if (dirs.length > 0)
            //                tr_fler.find(".dir").html(dirs[dirs.length - 1]);
            //        }
            //    });
            //    fler.after(tr_fler);
            //}
            //
            var f_name = obj.siblings(".cur_file_name");
            if (f_name.length > 0) f_name.html(para.f_name || uni.translate("未上传"));
            else obj.after("<span class='cur_file_name' style='color:green;padding-left:5px;'></span>");
            var up_file = obj.siblings("input[name=up_file]");
            if (up_file.length > 0) up_file.val("");
            else obj.before("<input type='hidden' name='up_file'/>");
        });
        objs.click(function () {
            var pthis = $(this);
            var file = pthis.attr("file");
            if (uni.isNull(file)) { uni.msgBox("未指定上传域", null, null, "error"); return; }
            if (!$("#" + file).val()) { uni.msg.warning("未选择上传的文件"); return; }
			 //限制类型
            if (para.type) {
                var typearr = para.type.split(",");
                var FileExt = $("#" + file + "").val().replace(/.+\./, "");
                var flag = false;
                for (var i = 0; i < typearr.length; i++) {
                    if (FileExt == typearr[i]) {
                        flag = true;
                        break;
                    }
                }
                if (!flag) {
                    uni.msgBox("上传文件的格式不正确(支持:" + para.type+")", null, null, "error");
                    return;
                }
            }
            var act = pthis.attr("act") || "upload";
            var ren = pthis.attr("ren") || "";
            var limit = pthis.attr("limit") || "";
            var dir = pthis.attr("dir") || "";
            var url = pro.dir + "ajax/file.aspx?act=" + act + "&limit=" + limit + "&file=" + file + "&dir=" + dir + "&ren=" + ren;
            if (FormData && (!uni.isIE() || uni.getIEVer() > 9)) {
                var fd = new FormData();
                fd.append("fileToUpload", document.getElementById(file).files[0]);
                var xhr = new XMLHttpRequest();
                //完成
                xhr.addEventListener("load", function (evt) {
                    uni.hideWait();
                    if (evt.target.status == 200) {
                        var rlt = JSON.parse(evt.target.responseText);
                        if (rlt.data) {
                            pthis.attr("save_name", rlt.data.save);
                            pthis.attr("cur_name", rlt.data.name);
                            pthis.siblings(".cur_file_name").html(uni.translate("已上传 ") + rlt.data.name);
                            pthis.siblings("input[name=up_file]").val(rlt.data.save);
                            pthis.siblings("input.up_file").val(rlt.data.save);
                        }
                        pro.ckV(rlt, suc, fail);
                    }
                    else {
                        uni.msgBox("出现异常，请刷新页面重试。", null, null, "warning");
                    }
                }, false);
                //错误
                xhr.addEventListener("error", function (evt) {
                    uni.hideWait();
                    uni.msgBox("出现异常，请刷新页面重试。", null, null, "warning");
                }, false);
                xhr.open("POST", url);
                uni.showWait();
                xhr.send(fd);
            }
            else {
                pthis.ajaxStart(function () {
                    uni.showWait();
                }).ajaxComplete(function () {
                    uni.hideWait();
                });
                $.ajaxFileUpload({
                    url: url,
                    secureuri: false,
                    fileElementId: file,
                    dataType: 'json',
                    success: function (rlt) {
                        if (rlt) {
                            rlt.obj = this;
                            if (rlt.data) {
                                pthis.attr("save_name", rlt.data.save);
                                pthis.attr("cur_name", rlt.data.name);
                                pthis.siblings(".cur_file_name").html(uni.translate("已上传 ") + rlt.data.name);
                                pthis.siblings("input[name=up_file]").val(rlt.data.save);
                                pthis.siblings("input.up_file").val(rlt.data.save);
                            }
                        }
                        pro.ckV(rlt, suc, fail);
                    },
                    error: function (err) {//（IE11）未知情况下也会触发error 暂时靠检查参数规避
                        var rlt = {};
                        var pre = $("<div>" + err.responseText + "</div>").find("pre");//谷歌浏览器会带pre标签
                        if (pre.length > 0) {
                            if (pre.html())
                                rlt = eval('(' + pre.html() + ')');
                        }
                        else if (err.responseText) {
                            rlt = eval('(' + err.responseText + ')');
                        }
                        if (rlt.ret == 1)
                            this.success(rlt);
                        else
                            uni.msgBox("出现异常，请刷新页面重试。", null, null, "warning");
                    }
                });
            }
        });
    },
    //简易状态条 obj来自devResvState
    stateSlider: function (obj, para) {
        if (obj.open.length < 2 || !obj.date) return;
        if (!para) para = {};
        var now = new Date();
        var date = obj.date;
        var panel = $("<div class='ss-panel'/>");
        $(this).html(panel);
        var open_start = parseInt(obj.open[0].replace(':', ''), 10);
        var open_end = parseInt(obj.open[1].replace(':', ''), 10);
        //标尺表
        var h_start = Math.floor(open_start / 100);
        var h_end = Math.ceil(open_end / 100);
        var width = para.width || panel.width();
        var nw = parseInt(width / (h_end - h_start));
        width = nw * (h_end - h_start);
        panel.width(width + 1);//重置面板宽度 需+1px表格边框
        var tbl = $("<div class='ss-tbl'></div>");
        var table = "<table class='ss-table'><tr>";
        for (var i = h_start; i < h_end; i++) {
            table += "<td style='width:" + (nw - 1) + "px'>" + uni.num2Str(i) + "</td>";
        }
        table += "</tr></table>";
        tbl.html(table);
        //状态版面
        var sp = $("<div class='ss-state-panel'></div>");
        var sum = (h_end - h_start) * 60;
        var m_left = nw * ((open_start % 100) / 60);
        var m_right = nw * (((60 - (open_end % 100)) % 60) / 60);
        sp.css("margin-left", m_left)
        .css("margin-right", m_right);
        //tip与状态条
        var tips = $('<div class="ss-tips"></div>').appendTo(sp);
        var slider = $("<div class='ss-slider'></div>").appendTo(sp);
        var arr = obj.ts.concat(obj.cls);
        var begin = uni.str2m(obj.open[0]);
        var terminal = uni.str2m(obj.open[1]);
        var op_start = date + " " + obj.open[0];
        var op_end = date + " " + obj.open[1];
        //今日过期时间
        if (date == now.format("yyyy-MM-dd")) {
            var m_start = uni.str2m(obj.open[0]);
            var m_end = now.getHours() * 60 + now.getMinutes();
            var w = nw * ((m_end - m_start) / 60);
            var bar = $("<div class='ss-bar' style='background:#ccc;left:0;width:" + w + "px'/>");
            slider.append(bar);
        }
        //状态条
        for (var i = 0; i < arr.length; i++) {
            var v = arr[i];
            if (!v.start || !v.end) continue;
            if (obj.islong && (uni.compareDate(v.end, op_start) < 0 || uni.compareDate(v.start, op_end) > 0)) continue;//长期 过滤当日以外
            if (uni.compareDate(v.end, now, "m") < 0) continue;//过滤今日已过期
            var start;
            var end;
            if (uni.compareDate(op_start, v.start, "m") > 0)//早于开始
                start = obj.open[0];
            else
                start = v.start.split(' ')[1];
            if (uni.compareDate(op_end, v.end, "m") < 0)//晚于结束
                end = obj.open[1];
            else
                end = v.end.split(' ')[1];
            var m_start = uni.str2m(start);
            var m_end = uni.str2m(end);
            var left = nw * ((m_start - begin) / 60);
            var w = nw * ((m_end - m_start) / 60);
            var bar = $("<div class='ss-bar' style='left:" + left + "px;width:" + w + "px'/>");
            slider.append(bar);
            //tip
            if (w > 35)//大于35像素显示开始tip
                tips.append('<div class="ss-tooltip" style="left: ' + (left - 17) + 'px;"><div class="ss-tooltip-inner">' + start + '</div><div class="ss-tooltip-arrow"></div></div>');
            if (w > 10)//大于10像素显示结束tip
                tips.append('<div class="ss-tooltip" style="left: ' + (left + w - 17) + 'px;"><div class="ss-tooltip-inner">' + end + '</div><div class="ss-tooltip-arrow"></div></div>');
        }
        //初始化
        if (para.start && para.end) {
            if (typeof (para.start) == "string") {
                drawDynBar(para.start, para.end);
            }
            else if (typeof (para.start) == "object" && $(para.start).is("input[type=text],select")) {
                var $start = $(para.start);
                var $end = $(para.end);
                var isSelect = $start.is("select");
                $start.change(function () {
                    var st = isSelect ? $start.children("option:selected").text() : $start.val();
                    var en = isSelect ? $end.children("option:selected").text() : $end.val();
                    drawDynBar(st, en);
                });
                $(para.end).change(function () {
                    var st = isSelect ? $start.children("option:selected").text() : $start.val();
                    var en = isSelect ? $end.children("option:selected").text() : $end.val();
                    drawDynBar(st, en);
                });
                $start.trigger("change");
            }
        }
        panel.append(sp);
        panel.append(tbl);
        function drawDynBar(start, end) {
            if (!start || !end || start == end) {
                sp.find(".ss-dyn").remove();
                return;
            }
            var m_start = uni.str2m(start);
            var m_end = uni.str2m(end);
            var left = nw * ((m_start - begin) / 60);
            var w = nw * ((m_end - m_start) / 60);
            sp.find(".ss-dyn").remove();
            slider.append("<div class='ss-bar ss-dyn' style='left:" + left + "px;width:" + w + "px'/>");
            if (w > 35)
                tips.append('<div class="ss-tooltip ss-dyn" style="left: ' + (left - 17) + 'px;"><div class="ss-tooltip-inner">' + start + '</div><div class="ss-tooltip-arrow"></div></div>');
            if (w > 10)
                tips.append('<div class="ss-tooltip ss-dyn" style="left: ' + (left + w - 17) + 'px;"><div class="ss-tooltip-inner">' + end + '</div><div class="ss-tooltip-arrow"></div></div>');
        }
    },
    //必填项目+类must 应许空+类allow_null  格式验证+data-reg（html5）
    mustItem: function (para) {
        para = para || {};
        var its = $(".must", this);
        for (var i = 0; i < its.length; i++) {
            var pthis = $(its[i]);
            var ipt;
            if (pthis.is("input[type=text],textarea,select")) ipt = pthis;
            else ipt = pthis.find("input[type=text],textarea,select");
            if (ipt.length > 0 && ipt.is(":visible")) {
                if (!ipt.hasClass("allow_null") && (ipt.val()).length == 0) {
                    ipt.addClass("must_it").change(function () { $(this).removeClass("must_it"); });
                    var msg=ipt.data("msg");
                    if(msg){
                        uni.msgBox(msg);
                    }
                    else if (!para.clsMsg) {
                        uni.msgBox(uni.translate("还有未填的项目"));
                    }
                    return false;
                }
                if ((ipt.val()).length > 0 && ipt.data("reg")) {
                    var reg = ipt.data("reg");
                    if (reg == "email") reg = /[_a-zA-Z\d\-\.]+@[_a-zA-Z\d\-]+(\.[_a-zA-Z\d\-]+)+$/;//邮箱
                    else if (reg == "number") reg = /^[0-9]*$/;//数字
                    if (!reg.test(ipt.val())) {
                        ipt.addClass("must_it").change(function () { $(this).removeClass("must_it"); });
                        var msg=ipt.data("ckmsg");
                        if(msg){
                            uni.msgBox(msg);
                        }
                        else if (!para.clsMsg) {
                            uni.msgBox(uni.translate("内容格式不正确"));
                        }
                        return false;
                    }
                }
            }
            pthis.removeClass("must_it");
        };
        return true;
    },
    //暂时未用
    checkLength: function (para) {
        var list = $("textarea[maxlength]", this);
        for (var i = 0; i < list.length; i++) {
            var area=$(list[i]);
            var len = area.attr("maxlength");
            if (area.val().length > len) {
                area.css("border-color", "red").one("onchange", function () {
                    $(this).css("border-color", "");
                });
                uni.msgBox(uni.translate("字数不得超出："+len));
                return false;
            }
        }
        return true;
    },
    //时间选择
    timePicker: function (para) {
        if (!para) para = {};
        var pickers = $(this);
        pickers.each(function () {
            var p = $(this);
            if (p.is("input")) {
                var c = getControl(p);
            }
        });
        function getControl(v) {
            var o_start = (para.open_start || "00:00").split(":");
            var o_end = (para.open_end || "23:59").split(":");
            var st = parseInt(o_start[0], 10);
            var en = parseInt(o_end[0], 10);
            var h = $("<select class='tpick_sel tpick_h' style='width:45px;'/>");
            for (var i = st ; i <= en ; i++) {
                h.append("<option>" + uni.num2Str(i) + "</option>");
            }
            var m = $("<select class='tpick_sel tpick_m' style='width:45px;'></select>");
            var u = para.unit || 5;
            for (var j = 0; j < 60; j++) {
                if (j % u == 0) {
                    m.append("<option>" + uni.num2Str(j) + "</option>");
                }
            }
            //检查开放时间
            h.change(function () {
                var val = parseInt(h.val(), 10);
                if (val == st) {
                    m.children().each(function () {
                        var t = $(this);
                        if (parseInt(t.html(), 10) < parseInt(o_start[1], 10))
                            t.hide();
                        else
                            t.show();
                    });
                }
                else if (val == en) {
                    m.children().each(function () {
                        var t = $(this);
                        if (parseInt(t.html(), 10) > parseInt(o_end[1], 10))
                            t.hide();
                        else
                            t.show();
                    });
                }
            });

            var span = $("<span class='pro_tpick'></span>");
            span.append(h).append(":").append(m);
            span.children("select").change(function () {
                v.val(h.val() + ":" + m.val());
                v.trigger("change");
            });
            v.after(span).hide();
            return span;
        }
    },
    //相册 列表区 .img_thumb 图片区 .img_large
    album: function () {
        var pthis = $(this);
        pthis.addClass("pro_album");
        $(".img_thumb a", pthis).click(function () {
            var thumbimgurl = $(this).children().attr('src');
            var largeimagenurl = thumbimgurl.replace("", "");
            $(".img_large img", pthis).attr('src', largeimagenurl);
            $(".img_thumb a", pthis).each(function () {
                if ($(this).hasClass('cur')) {
                    $(this).removeClass('cur');
                };
            })
            $(this).addClass('cur');
        })
        $(".img_thumb a:first", pthis).trigger("click");
    },
    //backtop
    backtop: function () {
        var pthis = $(this);
        pthis.addClass("pro_back_top");
        pthis.click(uni.backTop);
        $(window).scroll(function () {
            if ($(window).scrollTop() > 120)
                pthis.fadeIn('300');
            else
                pthis.fadeOut('300');
        });
        pthis.html("<span class='glyphicon glyphicon-arrow-up arrow'></span>");
    }
});
//筛选
(function ($) {
    var dft = {
        multi: false
    };
    $.fn.filterItem = function (callback, options) {
        var panel = $(this);
        var backFilter;
        var pop = false;
        var opt = $.extend(true, {}, dft, options);
        backFilter = callback;
        $(".it", panel).click(function () {
            var it = $(this);
            var ck = $("input[type=checkbox],input[type=radio]", this);
            if (!opt.multi) {
                it.siblings(".it").each(function () {
                    $(this).removeClass("f_sel");
                    $("input[type=checkbox],input[type=radio]", this).attr('checked', false);
                })
            }
            if (it.hasClass("f_sel")) {
                it.removeClass("f_sel");
                ck.attr('checked', false);
            }
            else {
                it.addClass("f_sel");
                ck.attr('checked', true);
            }
            pop = true;
        });
        $(".sub_filter", panel).click(function () {
            backFilter(getFilter());
        });
        $("select.auto", panel).change(function () {
            backFilter(getFilter());
        });
        $("select[affect]", panel).each(function () {
            var pthis = $(this);
            var o = pthis.attr("affect");
            var its = $("[key=" + o + "]", panel);
            if (its.is("select")) pthis.items = $(its.html());
            pthis.change(function () {
                var arr = [];
                arr.push(pthis.val());
                affect(pthis, arr, its);
            });
        });
        $(".its[affect]", panel).each(function () {
            var pthis = $(this);
            var its = $("[key=" + pthis.attr("affect") + "]", panel);
            if (its.is("select")) pthis.items = $(its.html());
            pthis.click(function () {
                var arr = [];
                var sel = pthis.find(".it.f_sel");
                for (var i = 0; i < sel.length; arr.push(sel.attr('value')), i++);
                affect(pthis, arr, its);
            });
        });
        function affect(pthis, arr, its) {
            if (its.is("select")) {
                var items = pthis.items;
                if (!items) return;
                its.html("");
                $.each(items, function () {
                    it = $(this);
                    var na = it.html();
                    var dep = it.attr("depend");
                    if (arr.length == 0 || uni.isInArray("", arr) || uni.isInArray("0", arr) || uni.isInArray(dep, arr) || !dep || dep == "0")
                        its.append(it.clone());
                });
                its.val("");
            }
            else {
                $(".it", its).each(function () {
                    it = $(this);
                    var dep = it.attr("depend");
                    if (arr.length == 0 || uni.isInArray("", arr) || uni.isInArray("0", arr) || uni.isInArray(dep, arr) || !dep || dep == "0")
                        it.show();
                    else {
                        it.removeClass("f_sel");
                        it.hide();
                    }
                });
            }
        }
        $(".its", panel).click(function () {//.it的点击冒泡到此处理（为了在.its[affect]后触发）
            if (pop) {
                backFilter(getFilter());
                pop = false;
            }
        });
        return getFilter;
        function getFilter() {
            var filter = {};
            $(".its", panel).each(function () {
                var fl = $(this);
                var key = fl.attr("key");
                if (!key) return true;
                filter[key] = "";
                var list = $(".f_sel", fl);
                var len = list.length - 1;
                list.each(function (i) {
                    filter[key] += $(this).attr('value') + (i < len ? "," : "");
                });
            });
            $("input[type=text],input[type=hidden],select", panel).each(function () {
                var fl = $(this);
                var key = fl.attr("key");
                if (!key) return true;
                filter[key] = fl.val();
            });
            return filter;
        }
    }
})(jQuery);

//时间选择
(function ($, uni) {
    function toMinute(v) {
        return parseInt(v / 100) * 60 + (v % 100);
    }
    function toTime(v) {
        return parseInt(v / 60) * 100 + (v % 60);
    }
    function toTimeStr(v) {
        v = v + "";
        if (v.length == 3) v = "0" + v;
        return v.substr(v.length - 4, 2) + ":" + v.substr(v.length - 2);
    }
    function timeInt(v) {
        if (v.length > 5)
            v = v.substr(v.length - 5);
        var tmp = v.split(":");
        if (tmp.length < 2) return 0;
        return parseInt(tmp[0], 10) * 100 + parseInt(tmp[1], 10);
    }
    function absMin(v, obj) {
        var diff;
        for (var i in obj) {
            var d = parseInt(i) - v;
            if (diff == undefined) diff = d;
            else if (Math.abs(diff) - Math.abs(d) > 0)
                diff = d;
        }
        return v + (diff || 0);
    }
    function checkInCls(t, cls) {//关闭时间内
        if (cls.length > 0) {
            for (var i = 0; i < cls.length; i++) {
                if (t > cls[i].start && t < cls[i].end)
                    return true;
            }
        }
        return false;
    }
    function checkStartCls(t, cls) {//关闭时间的开始时间 作为开始时间选取无意义
        if (cls.length > 0) {
            for (var i = 0; i < cls.length; i++) {
                if (t == cls[i].start)
                    return true;
            }
        }
        return false;
    }
    function findClsEdge(t, cls) {
        var ret = 9999;
        if (cls.length > 0) {
            for (var i = 0; i < cls.length; i++) {
                var start = cls[i].start
                if (t <= start && start < ret)
                    ret = start;
            }
        }
        return ret;
    }
    $.fn.extend({
        resvTimeClick: function ($endTime, para, $endDate) {
            if (!para || !uni.isNoNull([
                para.date,//当前日期
                para.openStart,
                para.openEnd,
                para.latest,
                para.earliest,
                para.max,
                para.min
            ])) {
                uni.msgBox("缺少参数", null, null, "error");
                uni.log.set("msg", "缺少参数/pro_resvTimeClick");
                return;
            }
            var hstart = $(this);
            var hend = $($endTime);
            var open_start = para.openStart ? timeInt(para.openStart) : 0;//开放时间 开始
            var open_end = para.openEnd ? timeInt(para.openEnd) : 2359;//开放时间 结束
            var latest = (para.latest && parseInt(para.latest) < 1440) ? parseInt(para.latest) : 0;//最迟提前
            var earliest = para.earliest ? parseInt(para.earliest) : 1440;//最早提前
            var min = para.min ? parseInt(para.min) : 0;//最少预约时间
            var max = para.max ? parseInt(para.max) : 1440;//最多预约时间
            var unit = para.unit ? parseInt(para.unit) : 10;//时间粒度
            var dft = para.span ? parseInt(para.span) : 0;//初始时间跨度
            var dft_sel = para.start ? timeInt(para.start) : open_start;//初始选中时间
            var dft_end = para.end ? timeInt(para.end) : 0;//初始结束时间
            //var fix = para.fix;//选时限制集合 格式{start1:end1,start2:end2...}或{start1:[end1,end2...],start2:[end1,end2...]...}
            var cls = [];
            if (para.cls && para.ts) {
                var temp_cls;
                if (para.allowLong == false) {//必须指明不是长期  (临时兼容长期)
                    if ((para.limit & 1024) > 0) {//预约规则为不检测冲突 则过滤可多选时段
                        temp_cls = para.cls;
                        for (var i = 0; i < para.ts.length; i++) {
                            if (para.ts[i].occupy) temp_cls.push(para.ts[i]);
                        }
                    }
                    else {
                        temp_cls = para.cls.concat(para.ts);//关闭时间 繁忙时段  对象数组[{start,end}]
                    }
                }
                else
                    temp_cls = para.cls;
                for (var i = 0; i < temp_cls.length; i++) {
                    var c = {};
                    c.start = timeInt(temp_cls[i].start);
                    c.end = timeInt(temp_cls[i].end);
                    if (para.alter && dft_sel == c.start) continue;//如果是修改 过滤掉当前预约时段
                    cls.push(c);
                }
            }
            //if (uni.isEmpty(fix)) fix = null;
            //if (fix) dft_sel = absMin(dft_sel, fix);//存在限制 重置默认值为最接近值
            var tmp = hstart.siblings(".tmp_end");
            if (tmp.length == 0) {
                tmp = $("<select style='display:none;' class='tmp_end'/>");
                hstart.after(tmp);
            }
            var hd_start = hstart.siblings(".hd_start");
            if (hd_start.length == 0) {
                hd_start = $("<input type='hidden' name='start' class='hd_start'/>");
                hstart.before(hd_start);
            }
            else
                hd_start.val("");
            var hd_end = hstart.siblings(".hd_end");
            if (hd_end.length == 0) {
                hd_end = $("<input type='hidden' name='end' class='hd_end'/>");
                hstart.before(hd_end);
            }
            else
                hd_end.val("");
            hstart.html("").unbind();
            hend.html("").unbind();
            tmp.html("");
            var ustart = open_start;
            var uend = open_end;
            var m_open_start = toMinute(open_start);
            var today = new Date();
            var dt = today.format("yyyy-MM-dd");
            if (dt == para.date) {
                var now = parseInt(today.format("HHmm"));
                var m_now = toMinute(now);
                var sp = m_now - m_open_start;
                if (sp > 0 && now < open_end) {
                    var u = m_now % unit;
                    if (u > 0)
                        sp = sp - u + unit;
                    ustart = toTime(m_open_start + sp);
                }
            }
            var mustart = toMinute(ustart);
            var muend = toMinute(uend);
            var m_dft_sel = toMinute(dft_sel);
            for (var i = mustart; i <= muend; i += unit) {
                var it = toTime(i);
                if (checkInCls(it, cls)) continue;//在关闭时间内
                var m_sp = i - m_dft_sel;
                if (0 <= m_sp && m_sp < unit)
                    dft_sel = it;
                var opt = "<option value='" + it + "'>" + toTimeStr(it) + "</option>";
                if (!checkStartCls(it, cls))//过滤关闭时间的开始时间 过滤限制集合 && (!fix || fix[it])
                    hstart.append(opt);
                tmp.append(opt);
            }
            hstart.val(dft_sel);
            if (parseInt(hstart.val()) != dft_sel) { var glinter = setInterval(glint, 500); setTimeout(clearGlint, 2500); }//闪烁
            var dftEnd = dft_end > 0 ? dft_end : (toTime(toMinute(dft_sel) + dft));
            tmp.val(dftEnd);
            hstart.change(function () {
                var val = parseInt($(this).val());
                var h = toMinute(val);
                //若支持长期para.allowLong 将撤销以下三种限制 (临时兼容长期)
                var edge = para.allowLong ? 9999 : findClsEdge(val, cls);//寻找允许时间的边界
                var st = para.allowLong ? open_start : toTime(h + min);//结束时间上限
                var en = para.allowLong ? open_end : toTime(h + uni.backMin([max, toMinute(open_end) - h]));//结束时间下限
                $("option", tmp).each(function () {
                    var v = parseInt($(this).val());
                    if (v > en || v < st || v > edge)// || (fix && fix[val] != v)
                        $(this).removeClass("v");
                    else
                        $(this).addClass("v");
                });
                hend.html($("option.v", tmp).clone());
                var sel = parseInt(tmp.val());
                if (sel > en || sel < st) {
                    sel = $("option:first", hend).val();
                    hend.css("border-color", "orange");
                }
                else {
                    hend.css("border-color", "");
                }
                tmp.val(sel);
                hend.val(sel);
                hd_start.val(para.date + " " + toTimeStr(hstart.val()));
                var end_date = uni.isNull($endDate) ? para.date : $endDate.val();
                hd_end.val(end_date + " " + toTimeStr(hend.val()));
                if (hend.html() == "") {
                    hend.css("border-color", "red");
                    hd_end.val("");
                    uni.msg.warning("缺少结束时间，请检查预约规则");
                }
            });
            hend.change(function () {
                $(this).css("border-color", "");
                tmp.val(hend.val());
                var end_date = uni.isNull($endDate) ? para.date : $endDate.val();
                hd_end.val(end_date + " " + toTimeStr(hend.val()));
            });
            if ($endDate) $endDate.change(function () { hend.trigger("change"); });
            hstart.trigger("change");
            //闪烁
            function glint() {
                hstart.css("border-color", "red");
                setTimeout(glint2, 250);
            }
            function glint2() {
                hstart.css("border-color", "");
            }
            function clearGlint() {
                hstart.css("border-color", "");
                window.clearInterval(glinter);
            }
        }
    })

})(jQuery, uni);
//-------------------------------初始化-----------------
$(function () {
    $('.logout').click(function () {
        var url = $(this).attr("url");
        pro.j.lg.logout(url);
    });
    if ($.fn.tooltip)
        $("[title]").tooltip();
    if ($.fn.button)
        $('.button').button();
    //子tr和li元素列表双色交替背景
    $('.zebra').zebra();
    //输入框提示
    $("input.hint").hint();
    $("body").on("uni_hr_load_success", function () { $("input.hint").hint(); });
});