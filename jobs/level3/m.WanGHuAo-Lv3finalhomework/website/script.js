<script>
    vm = new Vue({
        el:"#app",
        data:{
            modal:{
                show:false,
                isLoading:false,
                title:'',
                url:'',
                content:'',
                msg:''
            },
            showMenu:false,
            chozen:'all',
            editorMode:false,
            vids:[],
        },
        methods:{
            logIn:function () {
                var self = this;
                reqwest({
                    url:'/api/token-auth',
                    type:'json',
                    method:'post',
                    data:{
                        username:'admin',
                        password:'admin12345',
                    },
                    success:function (resp) {
                        console.log(resp);
                        Cookies.set('token',resp.token);
                        self.getData()
                    },

                })
            },
            logOut:function () {
                var self = this;
                Cookies.remove('token')
            },
            modalSwitch:function () {
                this.modal.show = !this.modal.show
            },
            editorsChoice:function (vid) {
                var self = this;
                var id = vid.id
                reqwest({
                    url:'/api/videos/' + id,
                    type:'json',
                    method:'put',
                    data:{
                        editors_choice:true,
                        title:vid.title,
                        content:vid.content,
                        url_image:vid.url_image,
                    },
                    success:function (resp) {
                        console.log(resp);
                        self.getData()
                    },

                })
            },
            deleteCard:function (vid) {
                var self = this;
                var id = vid.id
                reqwest({
                    url:'/api/videos/' + id,
                    type:'json',
                    method:'delete',
                    success:function (resp) {
                        console.log(Cookies.get('token'));
                        console.log(resp);
                        self.getData()
                    },

                })
            },
            // ==== HERE ====
            getData:function () {
                var self = this;
                reqwest({
                    url:'/api/videos/',
                    type:'json',
                    success:function (resp) {
                        console.log(resp);
                        self.vids = resp

                    },

                })
            },
            // ==== HERE ====
            sendData:function () {
                var self = this;
                self.modal.isLoading = !self.modal.isLoading
                // 使 segment 变成加载状态
                reqwest({
                    url:'/api/videos/',
                    method:'post',
                    type:'json',
                    data:{
                        title:self.modal.title,
                        url_image:self.modal.url,
                        content:self.modal.content
                    },
                    success:function (resp) {
                        console.log(resp);
                        self.modal.isLoading = !self.modal.isLoading
                        // 如果取回数据成功在把加载状态切换回来
                        self.modal.msg = resp.status
                        self.modalSwitch()
                        // 关闭弹窗
                        self.getData()
                    },
                    error:function (err) {
                        console.log(err);
                        self.modal.msg = err.status
                        self.modal.isLoading = !self.modal.isLoading

                    }

                })
            }
        },
        computed:{
            filtered:function () {
                var self = this
                if (self.chozen == 'editors_choice') {
                    var newList =self.vids.filter(function (vid) {
                            return vid.editors_choice == true
                        })
                    return newList
                } else {
                    return self.vids
                }
            },
            canScroll:function () {
                if (this.modal.show) {
                    return 'unscrollable'
                } else {
                    return ''
                }
            },
            fadeInOut:function () {
                if (this.modal.show) {
                    return ' fadeIn'
                } else {
                    return ' fadeOut'
                }
            },
            loadingOrNot:function () {
                if (this.modal.isLoading) {
                    return 'loading'
                } else {
                    return ''
                }
            },
            showMsg:function () {
                if (this.modal.msg == '201') {
                    return 'SUCCESS'
                } else if (this.modal.msg == '400') {
                    return 'SOMETHING WRONG'
                } else {
                    return 'Create a post'
                }
            }
        },
        transitions:{
            menu:{
                enterClass:'bounceInDown',
                leaveClass:'bounceOutUp'
            },

        },

        ready:function () {
            this.getData()
        }
    })
</script>
