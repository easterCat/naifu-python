// https://pm2.fenxianglu.cn/docs/general/configuration-file/
module.exports = {
    apps: [
        {
            name: "python-tag",
            script: "manage.py",
            interpreter: "python3",
            instances: "1",
            exec_mode: "fork",
            watch: false,
            restart_delay: 10000,
            cwd: "./",
        },
    ],
};
