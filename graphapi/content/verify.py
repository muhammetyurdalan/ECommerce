template = """<!DOCTYPE html>
                <html lang="tr">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Turuncu Beyaz Buton E-mail Template</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f7f7f7;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .email-container {
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #fff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                        }
                        .header {
                            background-color: #ff7f00;
                            color: #fff;
                            text-align: center;
                            padding: 20px;
                            border-radius: 8px 8px 0 0;
                        }
                        .content {
                            padding: 20px;
                            text-align: center;
                        }
                        .cta-button {
                            background-color: #ff7f00;
                            color: #fff;
                            font-size: 18px;
                            padding: 15px 30px;
                            text-decoration: none;
                            border-radius: 5px;
                            display: inline-block;
                            margin-top: 20px;
                            transition: background-color 0.3s;
                        }
                        .cta-button:hover {
                            background-color: #e76d00;
                        }
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <h1>Merhaba [name]</h1>
                        </div>
                        <div class="content">
                            <p>Hesabınızı doğrulamak için lütfen tıklayınız</p>
                            <a href="[endpoint]" class="cta-button">Doğrula</a>
                        </div>
                    </div>
                </body>
                </html>
"""