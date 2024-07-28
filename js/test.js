async function myFunction() {
    console.log("Start");

    // 使用 await 暂停函数执行，等待 Promise 解析完成
    await new Promise(resolve => {
        // setTimeout(() => {
        //     console.log("Inside setTimeout callback");
        //     resolve();
        // }, 2000); // 设置 2 秒延迟
        console.log("Inside setTimeout callback");
        resolve();
    });

    // 继续执行后续代码
    console.log("After await");

    // 在 setTimeout 回调函数中使用 await
    setTimeout(async () => {
        console.log("Inside nested setTimeout callback");
        await new Promise(resolve => setTimeout(resolve, 1000)); // 设置 1 秒延迟
        console.log("After nested await");
    }, 1000); // 设置 1 秒延迟

    console.log("End");
}

myFunction();
