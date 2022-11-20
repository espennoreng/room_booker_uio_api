import json

j = {
    "type": "service_account",
    "project_id": "roombooker-fdbf3",
    "private_key_id": "18e83a873328e1ee7d8128491b16ed68e4de192b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDEqMZOePH01Omp\ndFHLSrpCth6oO7aLj/XZ2hbKd0YxsCPU09BAJtlqAN6O8p/8wbyoD5O7L5UcjioI\n06r/EMK+9YEzyjgwkpkFIp5XAtJ+Y1WjFoEwNjfdcdgGxzsB8GJL0HapKx3PNLEr\n60mPOt9le2QwaLXaNRuigibAXEKeu3NjvH9EfdK5ZwZm04rmccgZrS4rTI3caJ/a\nJBbGA6BjoCfin6ne8JKsAHxd6BjGSkWhKYWPmogkTzdBA1DA5vCAXT7NDhxFOkvW\ntjA37pP4prcIeCjbB/os8mYbFzxayUc/GJGl8IfJae4dHvHJIMTBygHKkHgSituT\nxHWk91rVAgMBAAECggEACrfHDQZO64DCFlPqVEnHknSyAYm1lnAbXkriRJkRCIq4\nvTPpDOIBJeOTvZcwDHqzkTY+HyzF8+c0l8QPdPTBJF6lcsDh5JXMxKihGA1lkvFP\nfMKwekPuMgGvHBl2GBI1jTu4h9o7duxAfqwFV4rGG5YIvRGr3Y9Y6PeubHvqvpNQ\nwqdt6woHONivOe4bnSb8fYrJGzUVQ8NZYFRZPmUHFazBNzRAHRm40vk9KYH2RCBD\nqp1/YmfXJ9KRS0zmH/i1lSjDznXvm5+7Y88BkBGrwI8hqQUJc4X29+5Yg6qGkK3d\nuxVSzamjMiKwFvYl/TivP3ntUtKzu9zBsEiS4rtGuQKBgQDuy5cVGO6+6cVL7JT6\nbG05kgWP0SS/QUpBXh6efe45hT2F2Xp6eszFT/LUU2YdmcfStTJOA2nsH6IJVzdr\nfttPc52pCTb5xVXUjhBWy8PM9WCXNOl54g9M9VkwABKel3U/GGp3wFVasjC3opxb\nJzpiCB43CBN6gdXqzFDEHpVzOQKBgQDS1AQLpyVXFe6qLnYk4EDAl4K7XM/P1d1n\nqe4ZWba4+WHDRvvqCi7z7IHCAUnuRC11fiHTsgR0Q3t7uXBWgvCWHHAZ/I13pLno\npoecvtf9RWavKaQdr5oDrk2eGl6/QXXwnCYuLndwaJA57RTFKGsy7Oe1Idka1tuj\n/vZTBPbYfQKBgQCSR2DLabSGeomDku9H4DegdpS1nrZV+lbUaCV1jUrrLXWckrZ2\nZNcfX3QvIM+C/nrr1ld0dp7iKBaIhkbKsLEDoJ1JuP1WT83eIRBdOwE8gmui9KS5\nJwOcbwctYj4FrF4EQp6lsMoYfuNc+l2xcPxQpQxtRaM4/mPeKz6mhN2j8QKBgQCL\n9lzJL6nGarULHdUpHgde1DbiE/eSTrSxwUpkYf7ARi706QcMlL4fCYALP7fJClHz\nkkz6sU/rr3Em7jD5/euifDafyd5Q83bIUOXu1XOmnJBS8R4W5yEkGG9G6tLDvb2C\ngueF+Ssp4QD+s7n6OZ8RK92XjmUHQGSINxdoff8yMQKBgHSzdIq5xB5DnjmyOuyS\nyeHhRJ6mmsh7kX9rxArmBQHoTQjvjEIBfC82Q4q+FbsNGb/2Oqa7A/Ipurlh/Cwn\n8oj/A7B7JWSq1at9lMxA3ktrrUGXixSESMvWh2XE2g+P3BV1pjd7yuKK085HOVLa\nUI6W6aY9srzop4Juzy+Fq5pv\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-n9n5i@roombooker-fdbf3.iam.gserviceaccount.com",
    "client_id": "110334727911420794241",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-n9n5i%40roombooker-fdbf3.iam.gserviceaccount.com"
}

# Convert the json object to a string
json_string = json.dumps(j)

print(json_string)
