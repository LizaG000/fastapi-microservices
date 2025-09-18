using System.Text.RegularExpressions;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
var configuration = builder.Configuration;

var connectionString = $"Host={Environment.GetEnvironmentVariable("HOST") ?? "database"};" +
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

app.MapPost("/registrate", (User user) =>
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

    return Results.Ok(new
    {
        message = "Регистрация успешна",
        user
    });
});


app.Run();

public class User
{
    public string FirstName { get; set; } = string.Empty;
    public string LastName  { get; set; } = string.Empty;
    public int Age          { get; set; }
    public string Number    { get; set; } = string.Empty;
    public string Email     { get; set; } = string.Empty;
}