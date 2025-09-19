using System;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Text;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var httpClient = new HttpClient();
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
var configuration = builder.Configuration;

var connectionString = $"Host={Environment.GetEnvironmentVariable("HOST") ?? "localhost"};" +
                       $"Port={Environment.GetEnvironmentVariable("PORT") ?? "5432"};" +
                       $"Database={Environment.GetEnvironmentVariable("POSTGRES_DB") ?? "postgres"};" +
                       $"Username={Environment.GetEnvironmentVariable("POSTGRES_USER") ?? "postgres"};" +
                       $"Password={Environment.GetEnvironmentVariable("POSTGRES_PASSWORD" ?? "postgres")}";

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

var app = builder.Build();
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
    app.MapOpenApi();
}

//app.UseHttpsRedirection();

string GenerateRandomPassword(int length)
{
    const string chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";
    var random = new Random();
    return new string(Enumerable.Repeat(chars, length)
      .Select(s => s[random.Next(s.Length)]).ToArray());
}

app.MapPost("/registrate", async (User user, AppDbContext db) =>
{
    if (string.IsNullOrWhiteSpace(user.FirstName) || !Regex.IsMatch(user.FirstName, @"^[A-Za-zА-Яа-яЁё]+$"))
    {
        return Results.BadRequest(new { error = "Имя должно содержать только буквы." });
    }
    if (string.IsNullOrWhiteSpace(user.LastName) || !Regex.IsMatch(user.LastName, @"^[A-Za-zА-Яа-яЁё]+$"))
    {
        return Results.BadRequest(new { error = "Фамилия должна содержать только буквы." });
    }
    user.FirstName = char.ToUpper(user.FirstName[0]) + user.FirstName.Substring(1).ToLower();
    user.LastName = char.ToUpper(user.LastName[0]) + user.LastName.Substring(1).ToLower();

    if (user.Age < 18)
    {
        return Results.BadRequest(new { error = "Возраст должен быть не меньше 18 лет." });
    }
    if (!Regex.IsMatch(user.Number, @"^8\d{10}$"))
    {
        return Results.BadRequest(new { error = "Номер телефона должен начинаться с 8 и содержать 11 цифр." });
    }
    if (string.IsNullOrWhiteSpace(user.Email) ||
        !Regex.IsMatch(user.Email, @"^[^@\s]+@[^@\s]+\.[^@\s]+$"))
    {
        return Results.BadRequest(new { error = "Некорректный email." });
    }

    var entity = new UserEntity
    {
        FirstName = user.FirstName,
        LastName = user.LastName,
        Age = user.Age,
        Number = user.Number,
        Email = user.Email
    };
    var existingUser = await db.Users
    .Where(u => u.Number == user.Number || u.Email == user.Email)
    .FirstOrDefaultAsync();

    if (existingUser != null)
    {
        return Results.BadRequest(new { error = "Пользователь с таким номером телефона или email уже существует." });
    }

    var emailPart = user.Email.Split('@')[0];
    var login = emailPart+"+"+user.Number.Substring(user.Number.Length - 4, 4);
    var password = GenerateRandomPassword(8);

    var postData = new
    {
        login,
        password
    };

    var jsonContent = new StringContent(JsonSerializer.Serialize(postData), Encoding.UTF8, "application/json");


    var response = await httpClient.PostAsync("http://172.20.0.10:8000/api/user", jsonContent);

    if (response.IsSuccessStatusCode)
    {


        db.Users.Add(entity);
        await db.SaveChangesAsync();
        return Results.Ok(new
        {
            message = "Регистрация успешна, логин и пароль отправлены.",
            user,
            login,
        });
    }
    else
    {
        return Results.BadRequest(new { error = "Некорректные данные" });
    }
});


app.Run();

public class User
{
    public string FirstName { get; set; } = string.Empty;
    public string LastName  { get; set; } = string.Empty;
    public int Age          { get; set; } = 3;
    public string Number    { get; set; } = string.Empty;
    public string Email     { get; set; } = string.Empty;
}