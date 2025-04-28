<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Title</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap"
        rel="stylesheet">
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Space+Grotesk:wght@300..700&display=swap"
        rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,100..700;1,100..700&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Space+Grotesk:wght@300..700&display=swap"
        rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>


<body style="margin: auto; font-family: IBM Plex Sans;" class="my-4">
    
</body>


</html>


    <form hx-post="{{url_for('user.register')}}" hx-target="#alert">
        <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input type="text" name="user_name" class="form-control shadow-none" id="" required>
            <div class="form-text">This will be public in every one of your posts</div>
        </div>
        <div class="mb-3">
            <label class="form-label">Create an user id</label>
            <input type="text" name="user_id" class="form-control shadow-none" id="" required>
            <div class="form-text">Unique identificator to your account</div>
        </div>
        <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="text" name="user_email" class="form-control shadow-none" id="" required>
            <div class="form-text">If you allow it, users can contact you by this email</div>
        </div>
        <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="text" name="user_password" class="form-control shadow-none" id="" required>
            <div class="form-text"><a href="{{url_for('user.login')}}" class="link link-secondary">I already have an account</a></div>
        </div>
        <button type="submit" class="btn btn-dark">Create account</button>
    </form>